import os
import json
import math
import urllib.request
from datetime import date, datetime, timedelta
from urllib.parse import urlencode, quote_plus, unquote

from accounts.models import *
from mountains.models import *
from mountains.forms import ReviewCreationForm
from utils.distance import mountain_distance
from utils.weather import get_direction, process_air_data
from utils.helpers import serialize_courses 

import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.cache import cache


class MountainDetailView(LoginRequiredMixin, DetailView):
    model = Mountain
    template_name = 'mountains/mountain_detail.html'
    context_object_name = 'mountain'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        pk = self.kwargs.get('pk')

        # 산

        mountain = Mountain.objects.prefetch_related('post_set', 'post_set__postcomment_set').get(pk=pk)

        if not self.request.session.get(f'mountain_viewed_{mountain.pk}', False):
            Mountain.objects.filter(pk=mountain.pk).update(views=F('views') + 1)
            self.request.session[f'mountain_viewed_{mountain.pk}'] = True
            mountain.views += 1

        courses = mountain.course_set.all().prefetch_related('bookmarks')

        data = cache.get(f'mountain_detail_{hash(mountain.name)}')

        if not data:
            data = serialize_courses(courses, 'geom')
            cache.set(f'mountain_detail_{hash(mountain.name)}', data)
        
        distance = mountain_distance(user, mountain)

        # 리뷰
        reviews = Review.objects.filter(mountain=mountain).order_by('-created_at').select_related('user', 'mountain').prefetch_related('like_users', 'tags',)
        most_liked_review = reviews.annotate(num_likes=Count('like_users')).order_by('-num_likes').first()

        context.update({
            # 산 관련
            'mountain': mountain,
            'mountain_distance': distance,
            'courses': courses,
            'courses_data': data,

            # 리뷰 관련
            'form': ReviewCreationForm(),
            'reviews': reviews,
            'most_liked_review': most_liked_review,
        })

        return context

    
def get_weather_forecast(request, mountain_pk):
    now_weather_data = cache.get(f'now_weather_data_{mountain_pk}')
    if now_weather_data:
        return JsonResponse({
                'tem': now_weather_data['기온'],
                'hum': now_weather_data['습도'],
                'sky': now_weather_data['하늘상태'],
                'rain': now_weather_data['강수량'],
                'vec': now_weather_data['풍향'],
                'wsd': now_weather_data['풍속'],
                'now_time': now_weather_data['현재시각'],
                'sun': ['0700', '0800', '0900', '1000', '1100', '1200', '1300', '1400', '1500', '1600', '1700', '1800', '1900'],
                'moon': ['2000', '2100', '2200', '2300', '0000', '0100', '0200', '0300', '0400', '0500', '0600'],
        })
    else:
        try:
            mountain = Mountain.objects.get(pk=mountain_pk)
            # API 요청을 위한 URL과 파라미터 설정
            url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"

            serviceKey = os.environ['WEATHER_KEY']

            if not serviceKey:
                raise Exception("날씨 API 환경변수가 설정되어 있지 않습니다.")
            
            serviceKeyDecoded = unquote(serviceKey, 'UTF-8')
            now = datetime.now()
            today = datetime.today().strftime("%Y%m%d")
            y = date.today() - timedelta(days=1)
            yesterday = y.strftime("%Y%m%d")

            NX = 149            ## X축 격자점 수
            NY = 253            ## Y축 격자점 수

            Re = 6371.00877     ##  지도반경
            grid = 5.0          ##  격자간격 (km)
            slat1 = 30.0        ##  표준위도 1
            slat2 = 60.0        ##  표준위도 2
            olon = 126.0        ##  기준점 경도
            olat = 38.0         ##  기준점 위도
            xo = 210 / grid     ##  기준점 X좌표
            yo = 675 / grid     ##  기준점 Y좌표
            first = 0

            if first == 0 :
                PI = math.asin(1.0) * 2.0
                DEGRAD = PI/ 180.0
                
                re = Re / grid
                slat1 = slat1 * DEGRAD
                slat2 = slat2 * DEGRAD
                olon = olon * DEGRAD
                olat = olat * DEGRAD

                sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
                sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
                sf = math.tan(PI * 0.25 + slat1 * 0.5)
                sf = math.pow(sf, sn) * math.cos(slat1) / sn
                ro = math.tan(PI * 0.25 + olat * 0.5)
                ro = re * sf / math.pow(ro, sn)
                first = 1

            def mapToGrid(lat, lon, code = 0 ):
                ra = math.tan(PI * 0.25 + lat * DEGRAD * 0.5)
                ra = re * sf / pow(ra, sn)
                theta = lon * DEGRAD - olon
                if theta > PI :
                    theta -= 2.0 * PI
                if theta < -PI :
                    theta += 2.0 * PI
                theta *= sn
                x = (ra * math.sin(theta)) + xo
                y = (ro - ra * math.cos(theta)) + yo
                x = int(x + 1.5)
                y = int(y + 1.5)
                return x, y
            
            nx, ny = mapToGrid(mountain.geom.y, mountain.geom.x)

            if 0 < now.minute <= 59: # base_time와 base_date 구하는 함수
                if now.hour==0:
                    base_time = "2330"
                    base_date = yesterday
                else:
                    pre_hour = now.hour-1
                    if pre_hour < 10:
                        base_time = "0" + str(pre_hour) + "30"
                    else:
                        base_time = str(pre_hour) + "30"
                    base_date = today
            else:
                if now.hour < 10:
                    base_time = "0" + str(now.hour-1) + "30"
                else:
                    base_time = str(now.hour-1) + "30"
                base_date = today

            if now.hour < 10:
                now_time = '0'+str(now.hour)+'0'+'0'
            else:
                now_time = str(now.hour)+'0'+'0'

            queryParams = '?' + urlencode({ 
                    quote_plus('serviceKey') : serviceKeyDecoded,
                    quote_plus('base_date') : base_date,
                    quote_plus('base_time') : base_time,
                    quote_plus('nx') : nx,
                    quote_plus('ny') : ny,
                    quote_plus('dataType') : 'json',
                    quote_plus('numOfRows') : '1000'
                    })

            # API 요청 보내기
            response = requests.get(url + queryParams, verify=False)
            items = response.json().get('response').get('body').get('items') #데이터들 아이템에 저장
            now_weather_data = {}

            for item in items['item']:
                # 기온
                if item['category'] == 'T1H' and item['fcstDate'] == today and item['fcstTime'] == now_time:
                    now_weather_data['기온'] = item['fcstValue']
                # 습도
                if item['category'] == 'REH' and item['fcstDate'] == today and item['fcstTime'] == now_time:
                    now_weather_data['습도'] = item['fcstValue']
                # 하늘상태: 맑음(1) 구름많은(3) 흐림(4)
                if item['category'] == 'SKY' and item['fcstDate'] == today and item['fcstTime'] == now_time:
                    now_weather_data['하늘상태'] = item['fcstValue']
                # 1시간 동안 강수량
                if item['category'] == 'RN1' and item['fcstDate'] == today and item['fcstTime'] == now_time:
                    now_weather_data['강수량'] = item['fcstValue']
                # 풍향
                if item['category'] == 'VEC' and item['fcstDate'] == today and item['fcstTime'] == now_time:
                    now_weather_data['풍향'] = get_direction(item['fcstValue']) # utils 참조
                # 풍속
                if item['category'] == 'WSD' and item['fcstDate'] == today and item['fcstTime'] == now_time:
                    now_weather_data['풍속'] = item['fcstValue']
                # 현재시각
                if item['fcstDate'] == today and item['fcstTime'] == now_time:
                    now_weather_data['현재시각'] = now_time

            cache.set(f'now_weather_data_{mountain_pk}', now_weather_data, timeout=60 * 60)

            return JsonResponse({
                    'tem': now_weather_data['기온'],
                    'hum': now_weather_data['습도'],
                    'sky': now_weather_data['하늘상태'],
                    'rain': now_weather_data['강수량'],
                    'vec': now_weather_data['풍향'],
                    'wsd': now_weather_data['풍속'],
                    'now_time': now_weather_data['현재시각'],
                    'sun': ['0700', '0800', '0900', '1000', '1100', '1200', '1300', '1400', '1500', '1600', '1700', '1800', '1900'],
                    'moon': ['2000', '2100', '2200', '2300', '0000', '0100', '0200', '0300', '0400', '0500', '0600'],
            })
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def get_air(request, mountain_pk):
    fine_dust = cache.get(f'fine_dust_{mountain_pk}')
    ozone = cache.get(f'ozone_{mountain_pk}')
    region = cache.get(f'region_{mountain_pk}')
    if fine_dust and ozone and region:
        return JsonResponse({
            'region': region,
            'fine_dust': fine_dust,
            'ozone': ozone,
        })
    else:
        try: 
            mountain = Mountain.objects.get(pk=mountain_pk)
            today = datetime.today().strftime("%Y-%m-%d")
            yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

            url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth"
            serviceKey = os.environ['AIR_KEY']
            if not serviceKey:
                    raise Exception("AIR_KEY 환경 변수가 설정되어 있지 않습니다.")
            serviceKeyDecoded = unquote(serviceKey, 'UTF-8')

            queryParams = '?' + urlencode({ 
                quote_plus('serviceKey') : serviceKeyDecoded,
                quote_plus('returnType') : 'json',
                quote_plus('numOfRows') : '100',
                quote_plus('searchDate') : yesterday,
                quote_plus('InformCode') : 'PM10',
                })

            response = requests.get(url + queryParams, verify=False)

            if response.status_code != 200:
                raise Exception(f"API 요청이 실패하였습니다. 상태 코드: {response.status_code}")
            
            items = response.json().get('response').get('body').get('items') #데이터들 아이템에 저장

            air_data = {}
            for item in items:
                # 미세먼지
                if item['informCode'] == 'PM10' and item['informData'] == today:
                    air_data['미세먼지'] = item['informGrade']
                # 오존
                if item['informCode'] == 'O3' and item['informData'] == today:
                    air_data['오존'] = item['informGrade']

            fine_dust, ozone = process_air_data(air_data)
            region = get_formatted_region(mountain.region)

            cache.set(f'fine_dust_{mountain_pk}', fine_dust, timeout= 60 * 60 * 24)            
            cache.set(f'ozone_{mountain_pk}', ozone, timeout= 60 * 60 * 24)            
            cache.set(f'region_{mountain_pk}', region, timeout= 60 * 60 * 24)            

            return JsonResponse({
                'region': region,
                'fine_dust': fine_dust,
                'ozone': ozone,
            })
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def get_formatted_region(region):
    split_region = (region).split()
    region = split_region[0]

    special_chars = [',', '/']
    for char in special_chars:
        if region.endswith(char):
            region = region[:-1]
    return region

def get_news(request, mountain_pk):
    result = cache.get(f'news_{mountain_pk}')
    if result:
        return JsonResponse({'result': result})
    else:
        try:
            mountain = Mountain.objects.get(pk=mountain_pk)
            query = mountain.name
            encText = urllib.parse.quote(query.encode('utf-8'))

            client_id = os.environ['NAVER_NEWS_CLIENT_ID']
            client_secret = os.environ['NAVER_NEWS_SECRET']

            if not client_id or not client_secret:
                raise Exception("네이버 뉴스 API 환경 변수가 설정되어 있지 않습니다.")

            result = []
            for start in range(1, 6, 1):
                url = f'https://openapi.naver.com/v1/search/news.json?query={encText}&display={start}&sort=sim'

                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urllib.request.urlopen(request)
                rescode = response.getcode()

                if rescode == 200:
                    response_body = response.read().decode("utf-8")
                    items = json.loads(response_body)["items"]
                    for item in items:
                        item['title'] = item['title'].replace('&apos;', "'")
                        item['title'] = item['title'].replace('&quot;', "\"")
                        item['title'] = item['title'].replace('<b>', "")
                        item['title'] = item['title'].replace('</b>', "")
                    result.extend(items)
            
            result = [dict(t) for t in {tuple(d.items()) for d in result}]

            cache.set(f'news_{mountain_pk}', result, timeout= 60 * 60 * 24)

            return JsonResponse({'result': result})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@login_required
def mountain_likes(request, mountain_pk):
    mountain = get_object_or_404(Mountain, pk=mountain_pk)
    user = request.user
    if user in mountain.likes.all():
        mountain.likes.remove(user)
        is_liked = False
    else:
        mountain.likes.add(user)
        is_liked = True

    return JsonResponse({'is_liked': is_liked, 'like_count':mountain.likes.count()})    


@login_required
def bookmark(request, mountain_pk, course_pk):
    course = Course.objects.get(pk=course_pk)
    user = request.user
    is_bookmarked = user.bookmarks.filter(pk=course_pk).exists()
    if is_bookmarked:
        user.bookmarks.remove(course)
        is_bookmarked = False
    else:
        user.bookmarks.add(course)
        is_bookmarked = True
    context = {
        'is_bookmarked' : is_bookmarked,
    }
    return JsonResponse(context)
