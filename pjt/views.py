from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import ListView
from mountains.models import *
from accounts.models import *
from utils.distance import mountains_distance
import random
from django.core.cache import cache
from django.db.models import OuterRef, Subquery, Count

def index(request):
    return render(request, 'pjt/mainindex.html')


class MainView(ListView):
    template_name = 'pjt/main.html'
    context_object_name = 'mountains'
    model = Mountain

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        mountains = cache.get('main_mountains')
        
        if not mountains:   
            mountains = Mountain.objects.annotate(
                course_cnt=Subquery(
                    Course.objects.filter(mntn_name=OuterRef('name'))
                    .values('mntn_name')
                    .annotate(course_count=Count('mntn_name'))
                    .values('course_count')
                )
            )
            cache.set('main_mountains', mountains)

        # 1. 랜덤 유저의 좋아요 산 리스트
        all_users = User.objects.exclude(pk=user.pk)
        random_user_like_mountains = None
        random_user = None

        while all_users:
            random_user = random.choice(all_users)
            user_like_mountains = mountains.filter(likes=random_user)
            
            if user_like_mountains.exists():
                if len(user_like_mountains) < 6:
                    random_user_like_mountains = user_like_mountains
                else:
                    random_user_like_mountains = random.sample(list(user_like_mountains), 6)
                break
                
            all_users = all_users.exclude(pk=random_user.pk)

        if not all_users:
            random_user_like_mountains = None
            random_user = None

        # 2. 초보/고수 추천 산 리스트
        tags = [14, 15, 16, 18]
        filtered_mountains = mountains.filter(review__tags__pk__in=tags).distinct()

        ## top_tags에 [14, 15] 태그가 있는 산을 필터링합니다.
        low_lv_mountains = [mountain for mountain in filtered_mountains if any(tag in mountain.top_tags_pk for tag in [14, 15])]
        if len(low_lv_mountains) < 12:
            random_low_lv_mountains = low_lv_mountains
        else:
            random_low_lv_mountains = random.sample(list(low_lv_mountains), 12)

        ## top_tags에 [16, 18] 태그가 있는 산을 필터링합니다.
        high_lv_mountains = [mountain for mountain in filtered_mountains if any(tag in mountain.top_tags_pk for tag in [16, 18])]    
        if len(high_lv_mountains) < 12:
            random_high_lv_mountains = high_lv_mountains
        else:
            random_high_lv_mountains = random.sample(list(high_lv_mountains), 12)


        # 3. 로그인한 유저가 방문하지 않은 산 리스트
        visited_mountain_ids = VisitedCourse.objects.filter(user=user).values('mountain_id')
        not_visited_mountains = mountains.exclude(id__in=visited_mountain_ids)
        if len(not_visited_mountains) < 12:
            random_not_visited_mountains = not_visited_mountains
        else:
            random_not_visited_mountains = random.sample(list(not_visited_mountains), 12)


        # user_distacne 계산
        low_lv_mountains_distance = mountains_distance(user, low_lv_mountains)    
        high_lv_mountains_distance = mountains_distance(user, high_lv_mountains)    
        not_visited_mountains_distance = mountains_distance(user, random_not_visited_mountains)    
        user_like_mountains_distance = mountains_distance(user, random_user_like_mountains)    

        context = {
            'low_lv_mountains': zip(random_low_lv_mountains, low_lv_mountains_distance),
            'high_lv_mountains': zip(random_high_lv_mountains, high_lv_mountains_distance),
            'not_visited_mountains': zip(random_not_visited_mountains, not_visited_mountains_distance),
            'user_like_mountains': zip(random_user_like_mountains, user_like_mountains_distance),
            'random_user': random_user,
        }

        return context
    
