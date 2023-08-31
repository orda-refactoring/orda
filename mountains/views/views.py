import gpxpy, gpxpy.gpx, os, datetime
from mountains.models import *
from accounts.models import *
from mountains.forms import SearchForm
from utils.weather import get_weather, get_direction
from utils.distance import mountains_distance
from utils.helpers import serialize_courses
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, When, Case, Q
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.views.generic import ListView, FormView, View, DetailView
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import hashlib
from django.db.models import Prefetch


class SearchView(FormView):
    template_name = 'mountains/search.html'
    form_class = SearchForm
    success_url = 'mountains/mountain_list.html'

def mountain_list(request):
    user = request.user
    tags = request.GET.getlist('tags')
    sido = request.GET.get('sido')
    gugun = request.GET.get('gugun')
    search_query = request.GET.get('search_query')
    sort = request.GET.get('sort', None)
    page= request.GET.get('page', '1')

    mountains = Mountain.objects.all().prefetch_related('likes', 'review_set', 'course_set')

    filter_condition = Q()

    if sido and gugun:
        region_filter = Q(region__contains=sido)
        if '전체' not in gugun:
            region_filter &= Q(region__contains=gugun)
        filter_condition &= region_filter

    if tags:
        filtered_mountains = mountains.filter(review__tags__pk__in=tags).distinct()
        int_tags = list(map(int, tags))
        filtered_pks = []
        for filtered_mountain in filtered_mountains:
            top_tags_pk = filtered_mountain.top_tags_pk
            if any((tag_pk in top_tags_pk) for tag_pk in int_tags):
                filtered_pks.append(filtered_mountain.pk)
        filter_condition &= Q(pk__in=filtered_pks)

    if search_query:
        filter_condition &= Q(name__icontains=search_query)

    mountains = mountains.filter(filter_condition)
        
    if sort== 'likes':
        mountains = mountains.annotate(likes_count=Count('likes')).order_by('-likes_count')  # 좋아요순으로 정렬
    elif sort == 'reviews':
        mountains = mountains.annotate(reviews_count2=Count('review')).order_by('-reviews_count2') # 리뷰순으로 정렬
    elif sort == 'id':
        mountains = mountains.order_by('id')  # 가나다순으로 정렬
    elif sort== 'views':
        mountains = mountains.order_by('-views')  # 조회순으로 정렬
    elif sort == 'height':
        mountains = mountains.order_by('height') # 고도순으로 정렬

    per_page = 12
    paginator = Paginator(mountains, per_page)
    page_obj = paginator.get_page(page)

    distances = mountains_distance(user, page_obj)

    context = {
        'page_obj': page_obj,
        'mountain_data': zip(page_obj, distances),
    }
    return render(request, 'mountains/mountain_list.html', context)


class CourseListView(LoginRequiredMixin, ListView):
    template_name = 'mountains/course_list.html'
    context_object_name = 'courses'
    model = Course
    paginate_by = 5    

    def get_queryset(self):
        sort = self.request.GET.get('sort', '')

        mountain = cache.get(f'mountain_{self.kwargs["mountain_pk"]}')
        
        if not mountain:
            mountain = Mountain.objects.get(pk=self.kwargs['mountain_pk'])
            cache.set(f'mountain_{self.kwargs["mountain_pk"]}', mountain)

        queryset = Course.objects.filter(mntn_name=mountain).prefetch_related('bookmarks')
        queryset = sort_courses(queryset, sort)
        self.mountain = mountain
    
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        mountain = self.mountain
        
        page_number = self.request.GET.get('page')
        paginator = Paginator(queryset, self.paginate_by)
        page_obj = paginator.get_page(page_number)
            
        courses_data = cache.get(f'course_list_{hash(mountain.name)}_course')
        detail_data = cache.get(f'course_list_{hash(mountain.name)}_detail')

        if not courses_data or not detail_data:
            courses_data = serialize_courses(page_obj, 'geom')
            detail_data = {}
            for course in page_obj:
                course_detail = CourseDetail.objects.filter(crs_name_detail=course)
                detail_data[course.pk] = serialize_courses(course_detail, 'geom', 'waypoint_name', 'waypoint_category', attach=False)
                
                cache.set(f'course_list_{hash(mountain.name)}_course', courses_data)
                cache.set(f'course_list_{hash(mountain.name)}_detail', detail_data)

        context.update({
            'mountain': mountain,
            'courses': page_obj,
            'courses_data': courses_data,
            'detail_data': detail_data,
            'is_paginated': page_obj.has_other_pages(),
            'page_obj': page_obj,
        })
        return context     


def course_all_list(request):
    sido = request.GET.get('sido', '')
    gugun = request.GET.get('gugun', '')
    sort = request.GET.get('sort', None)
    page= request.GET.get('page', '1')
    per_page = 10

    mountains = cache.get(f'course_all_list')

    if mountains is None:
        mountains = Mountain.objects.all()
        cache.set(f'course_all_list', mountains)

    if sido and gugun:
        if ('광역시' in sido) or ('특별시' in sido):
            mountains = Mountain.objects.filter(Q(region__contains=sido))
        else:
            if '전체' in gugun:
                mountains = Mountain.objects.filter(Q(region__contains=sido))
            else:
                mountains = Mountain.objects.filter(Q(region__contains=sido) & Q(region__contains=gugun))

    courses = Course.objects.filter(mntn_name__in=mountains).select_related('mntn_name').prefetch_related('bookmarks')

    courses = sort_courses(courses, sort)

    paginator = Paginator(courses, per_page)
    page_obj = paginator.get_page(page)


    context = {
        'page_obj': page_obj,
    }
    return render(request, 'mountains/course_all_list.html', context)


class CourseDetailView(DetailView): # LoginRequiredMixin
    model = Course
    template_name = 'mountains/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_pk = self.kwargs['pk']

        # 캐싱
        course = cache.get(f'course_detail_{course_pk}')
        course_data = cache.get(f'course_detail_{course_pk}_course')
        detail_data = cache.get(f'course_detail_{course_pk}_detail')

        if not course:
            course = get_object_or_404(Course, pk=course_pk)
            cache.set(f'course_detail_{course_pk}', course, 86,400)
            
        if not course_data or not detail_data:
            course_detail = CourseDetail.objects.filter(crs_name_detail=course)

            course_data = serialize_courses([course], 'geom')
            detail_data = serialize_courses(course_detail, 'geom', 'waypoint_name', 'waypoint_category')
            cache.set(f'course_detail_{course_pk}_course', course_data)
            cache.set(f'course_detail_{course_pk}_detail', detail_data)

        mountain = course.mntn_name

        context.update({
            'mountain': mountain,
            'course': course,
            'course_data': course_data,
            'detail_data': detail_data,
        })
        return context
    

def sort_courses(courses, sort_option):
    if sort_option == 'bookmarks':
        return courses.annotate(bookmarks_count=Count('bookmarks')).order_by('-bookmarks_count')
    elif sort_option == 'hidden_time':
        return courses.order_by('hidden_time')
    elif sort_option == 'distance':
        return courses.order_by('distance')
    elif sort_option == 'id':
        return courses.order_by('id')
    elif sort_option == 'diff':
        return courses.annotate(
            diff_order=Case(
                When(diff='하', then=1),
                When(diff='중', then=2),
                When(diff='상', then=3),
                default=4
            )
        ).order_by('diff_order')
    else:
        return courses    


class gpxDownloadView(LoginRequiredMixin, View):
    def post(self, request, mountain_pk, course_pk):
        course = Course.objects.get(pk=course_pk)
        geom = course.geom
        name = course.crs_name_detail

        # GPX 파일 생성 및 변환
        gpx_data = self.create_gpx(geom, name)

        # 이메일 전송
        email = request.user.email
        if email:
            self.send_email(email, gpx_data, name)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

    def create_gpx(self, geom, name):
        # 등산 코스의 geom 데이터를 GPX 형식으로 변환하는 로직을 구현합니다.
        gpx = gpxpy.gpx.GPX()
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        for point in geom.coords:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude=point[1], longitude=point[0]))

        # GPX 데이터를 반환합니다.
        gpx_data = gpx.to_xml()
        return gpx_data    

    def send_email(self, email, gpx_data, name):
        email_subject = f'[오르다] {name} 등산 코스 GPX 파일'
        email_body = render_to_string('mountains/email.html', {'name': name})
        email_attachment = (f"{name.replace(' ', '_')}_course.gpx", gpx_data, "application/gpx+xml")

        email_message = EmailMessage(email_subject, email_body, os.getenv('DEFAULT_FROM_EMAIL'), [email])
        email_message.attach(*email_attachment)
        email_message.send()
        

@login_required        
def weather_forecast(request, pk):
    mountain = Mountain.objects.get(pk=pk)
    lat = mountain.geom.y
    lon = mountain.geom.x
    api_key = os.environ['OPEN_WEATHER_KEY']

    weather_data = get_weather(lat, lon, api_key)

    daily_data = {}  # 날짜별 데이터를 담을 딕셔너리

    for forecast in weather_data['list']:
        dt_txt = datetime.datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=9)
        date_key = dt_txt.strftime('%d일')  # 날짜를 key로 사용
        forecast['dt_txt'] = dt_txt.strftime('%H시')
        forecast['pop'] = int(forecast['pop'] * 100)
        forecast['wind']['deg'] = get_direction(str(forecast['wind']['deg']))

        if date_key not in daily_data:
            daily_data[date_key] = []  # 새로운 날짜의 데이터를 빈 리스트로 초기화

        daily_data[date_key].append(forecast)  # 해당 날짜에 데이터 추가

    context = {
        'mountain': mountain,
        'weather_data': weather_data,
        'daily_data': daily_data,
    }

    return render(request, 'mountains/weather_forecast.html', context)