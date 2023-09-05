import os, requests
from .forms import *
from .models import *
from mountains.models import Mountain, Course
from utils.level import level_dict
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model, update_session_auth_hash, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

def login(request):
    if request.user.is_authenticated:
        return redirect('main')
    
    if request.method == 'POST':
        form = CustomUserAuthenticationForm(request, request.POST)
        
        if form.is_valid():
            auth_login(request, form.get_user())
            # 이전 페이지 URL 가져오기
            previous_page = request.session.get('previous_page')
            if previous_page:
                del request.session['previous_page']
                return redirect(previous_page)
            else:
                return redirect('main')
    else:
        form = CustomUserAuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return render(request, 'pjt/mainindex.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('mountains:mountain_list')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)

            UserLocation.objects.create(user=user)

            return redirect('mountains:mountain_list')
        else:
            for key, error in list(form.errors.items()):
                print(key, error)
    else:   
        form = CustomUserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)


def check_username(request):
    if request.method == 'POST':        
        username = request.POST.get('username')
        if username:
            exists = User.objects.filter(username=username).exists()
            return JsonResponse({'exists': exists})
    return JsonResponse({'exists': False})


def profile(request, user_pk):
    User = get_user_model()
    person = User.objects.prefetch_related('followings', 'followers', 'liked_mountains', 'post_set', 'review_set', 'postcomment_set', 'visitedcourse_set', 'like_posts', 'bookmarks').get(pk=user_pk)
    posts = person.post_set.all().order_by('-created_at')
    reviews = person.review_set.select_related('mountain').all().order_by('-created_at')
    posts_comments = person.postcomment_set.count()
    visited_courses = person.visitedcourse_set.count()

    liked_posts = person.like_posts.all()
    liked_mountains = person.liked_mountains.all()
    bookmark_course = person.bookmarks.prefetch_related('mntn_name').all()
    print(bookmark_course[0].mntn_name)
    score = len(posts) * 30 + len(reviews) * 20 + visited_courses * 10 + posts_comments * 5
    level = person.level

    if level_dict[level]['max_score'] == 'MAX':
        expbar = 100
        restexp = 0
    else:
        now_score = score - level_dict[level]['min_score']
        expbar = (now_score / level_dict[level]['need_score']) * 100
        restexp = level_dict[level]['need_score'] - now_score

    context = {
        'person': person,
        'posts': posts,
        'reviews': reviews,
        'max_score': level_dict[level]['max_score'] ,
        'liked_posts': liked_posts,
        'liked_mountains': liked_mountains,
        'bookmark_course': bookmark_course,
        'score': score,
        'expbar': expbar,
        'restexp': restexp,
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def delete(request):
    if request.method == 'POST':
        request.user.delete()
        auth_logout(request)
        return render(request, 'pjt/mainindex.html')
    return render(request, 'accounts/delete.html')


@login_required
def password_change(request):
    if request.method == 'POST':
        form = CustomUserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:profile', request.user.pk)
    else:
        form = CustomUserPasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/password_change.html', context)


@login_required
def follow(request, user_pk):
    User = get_user_model()
    person  = User.objects.get(pk=user_pk)
    me = request.user

    if person != me:
        if me in person.followers.all():
            person.followers.remove(me)
            is_followed = False
        else:
            person.followers.add(me)
            is_followed = True
            
            follow_url = reverse('accounts:profile', kwargs={'user_pk': me.pk})
            follow_link = mark_safe(f'<a href="{follow_url}">{me.username}</a>')
            message = f'{follow_link}님이 당신을 팔로우합니다.'
            notification = Notification.objects.create(user=person, notification_type='팔로우', message=message)
            
        context = {
            'is_followed':is_followed,
            'followings_count':person.followings.count(),
            'followers_count':person.followers.count(),
            'followers': [{'username': f.username,'pk': f.pk} for f in person.followers.all()]
        }
        return JsonResponse(context)
    return redirect('accounts:profile', person.pk)


load_dotenv()
KAKAO_CLIENT_ID = os.environ.get('KAKAO_CLIENT_ID')
NAVER_CLIENT_ID = os.environ.get('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.environ.get('NAVER_CLIENT_SECRET')


def kakao_login(request):
    client_id = KAKAO_CLIENT_ID
    redirect_uri = 'http://127.0.0.1:8000/accounts/kakao/callback/'
    url = f'https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
    return redirect(url)


def kakao_callback(request):
    User = get_user_model()
    code = request.GET.get('code')
    if code:
        url = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': KAKAO_CLIENT_ID,
            'redirect_uri': 'http://127.0.0.1:8000/accounts/kakao/callback/',
            'code': code,
        }
        response = requests.post(url, data=data)
        token = response.json().get('access_token')
        if token:
            headers = {
                'Authorization': f'Bearer {token}',
            }
            response = requests.get('https://kapi.kakao.com/v2/user/me', headers=headers)
            user_info = response.json()

            kakao_user_id = user_info['id']

            user, created = User.objects.get_or_create(username=kakao_user_id)

            if created:
                user.kakao_user_id = kakao_user_id
                if 'kakao_account' in user_info and 'email' in user_info['kakao_account']:
                    user.email = user_info['kakao_account']['email']

                if 'properties' in user_info and 'profile_image' in user_info['properties']:
                    profile_image_url = user_info['properties']['profile_image']
                    # 앞부분을 잘라냄
                    filename = profile_image_url.replace('http://k.kakaocdn.net/dn/', '')
                    response = requests.get(profile_image_url)
                    if response.status_code == 200:
                        file_content = ContentFile(response.content)
                        user.profile_img.save(filename, file_content, save=True)
                user.save()
                auth_login(request, user)
                return redirect('accounts:update')
            else:
                auth_login(request, user)
                return redirect('main')
    return redirect('accounts:login')


def naver_login(request):
    client_id = NAVER_CLIENT_ID
    redirect_uri = 'http://127.0.0.1:8000/accounts/naver/callback/'
    url = f'https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&state=STATE_STRING'
    return redirect(url)


def naver_callback(request):
    User = get_user_model()
    code = request.GET.get('code')
    if code:
        url = 'https://nid.naver.com/oauth2.0/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': NAVER_CLIENT_ID,
            'client_secret': NAVER_CLIENT_SECRET,
            'redirect_uri': 'http://127.0.0.1:8000/accounts/naver/callback/',
            'code': code,
        }
        response = requests.post(url, data=data)
        token = response.json().get('access_token')
        if token:
            headers = {
                'Authorization': f'Bearer {token}',
            }
            response = requests.get('https://openapi.naver.com/v1/nid/me', headers=headers)
            user_info = response.json()

            naver_user_id = user_info['response']['id']

            user, created = User.objects.get_or_create(username=naver_user_id)

            if created:
                user.naver_user_id = naver_user_id
                if 'email' in user_info['response']:
                    user.email = user_info['response']['email']

                if 'profile_image' in user_info['response']:
                    profile_image_url = user_info['response']['profile_image']
                    # 앞부분을 잘라냄
                    filename = profile_image_url.replace('https://phinf.pstatic.net/contact/', '')
                    response = requests.get(profile_image_url)
                    if response.status_code == 200:
                        file_content = ContentFile(response.content)
                        user.profile_img.save(filename, file_content, save=True)
                user.save()
                auth_login(request, user)
                return redirect('accounts:update')
            else:
                auth_login(request, user)
                return redirect('main')
    return redirect('accounts:login')


def get_first_image_from_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    img_tag = soup.find('img')
    print(img_tag)
    if img_tag:
        return img_tag['src']
    else:
        return None
    

@login_required
def my_memories(request):
    mountains = cache.get('all_mountains')

    if not mountains:
        mountains = Mountain.objects.prefetch_related('course_set').all()
        cache.set('all_mountains', mountains)

    visited_courses = request.user.visited_courses.all()
    visited_mountains = (
        VisitedCourse.objects.filter(user=request.user)
        .values_list('mountain_name', flat=True)
        .distinct()
    )
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = Course.objects.get(id=course_id)

        if course in visited_courses:
            request.user.visited_courses.remove(course)
            is_visited = False

        else:
            VisitedCourse.objects.create(
                user=request.user,
                course=course,
                mountain_name=course.mntn_name,
                mountain_id=course.mntn_name.id,
            )

            request.user.adjust_user_level()

            is_visited = True

        context = {
            'is_visited' : is_visited,
            'message': 'Visited course toggled successfully.',
        }

        return JsonResponse(context)

    context = {
        'mountains': mountains,
        'visited_courses': visited_courses,
        'visited_mountains': visited_mountains,
    }
    return render(request, 'accounts/my_memories.html', context)


def notification(request):
    user = request.user
    notifications = user.notifications.all()
    notification_count = notifications.count()  
    return render(request, 'accounts/notification.html', {'notifications': notifications, 'notification_count': notification_count})


def notification_check(request, notification_pk):
    notification = Notification.objects.get(pk=notification_pk)
    notification.is_read = True
    notification.save()
    return JsonResponse({'success': True})  


def notification_delete(request, notification_pk):
    notification = Notification.objects.get(pk=notification_pk)
    notification.delete()
    return JsonResponse({'success': True}) 


@login_required
def save_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        user = request.user
        user_location, created = UserLocation.objects.get_or_create(user=user)
        user_location.latitude = latitude
        user_location.longitude = longitude
        user_location.save()

        return JsonResponse({'success': True})
    else:
        # 임시로 render함수 사용. 추후, JsonResponse로 수정할 예정
        return render(request, 'accounts/test_location.html')