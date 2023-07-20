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

        # 유저가 방문한 산들의 id 추출
        visited_mountain_ids = VisitedCourse.objects.filter(user=user).values('mountain_id')

        # 오른기억에 체크한 산을 제외한 나머지 산을 랜덤으로 추출한다.
        not_visited_mountains = Mountain.objects.exclude(id__in=visited_mountain_ids)
        random_not_visited_mountains = random.sample(list(not_visited_mountains), 12)

        context = {
            'not_visited_mountains': random_not_visited_mountains,
        }

        return context