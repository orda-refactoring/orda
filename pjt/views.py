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


        # 2. 초보/고수 추천 산 리스트

        # 리뷰에 14, 15, 16, 18 태그가 있는 산만 걸러낸다.
        filtered_mountains = Mountain.objects.filter(review__tags__pk__in = [14, 15, 16, 18])
        low_lv_mountains = 1        
        high_lv_mountains = 1        

        # 3. 로그인한 유저가 방문하지 않은 산 리스트
        visited_mountain_ids = VisitedCourse.objects.filter(user=user).values('mountain_id')
        not_visited_mountains = Mountain.objects.exclude(id__in=visited_mountain_ids)
        random_not_visited_mountains = random.sample(list(not_visited_mountains), 12)

        context = {
            'not_visited_mountains': random_not_visited_mountains,
        }

        return context
    
