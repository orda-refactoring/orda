from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import ListView
from mountains.models import *
from accounts.models import *
import random

def index(request):
    return render(request, 'pjt/mainindex.html')

class MainView(ListView):
    template_name = 'pjt/main.html'
    context_object_name = 'mountains'
    model = Mountain

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # 1. 랜덤 유저의 좋아요 산 리스트
        all_users = User.objects.exclude(pk=user.pk)
        if all_users:
            random_user = random.choice(all_users)
            user_like_mountains = Mountain.objects.filter(likes=random_user)
            if len(user_like_mountains) < 12:
                random_user_like_mountains = user_like_mountains
            else:
                random_user_like_mountains = random.sample(list(user_like_mountains), 12)
        else:
            random_user_like_mountains = None
            random_user = None

        # 2. 초보/고수 추천 산 리스트
        tags = [14, 15, 16, 18]
        filtered_mountains = Mountain.objects.filter(review__tags__pk__in=tags).distinct()

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
        not_visited_mountains = Mountain.objects.exclude(id__in=visited_mountain_ids)
        if len(not_visited_mountains) < 12:
            random_not_visited_mountains = not_visited_mountains
        else:
            random_not_visited_mountains = random.sample(list(not_visited_mountains), 12)

        context = {
            'low_lv_mountains': random_low_lv_mountains,
            'high_lv_mountains': random_high_lv_mountains,
            'not_visited_mountains': random_not_visited_mountains,
            'user_like_mountains': random_user_like_mountains,
            'random_user': random_user,
        }

        return context
    
