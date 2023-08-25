from django.urls import path
from .views import *

app_name = 'mountains'
urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),

    path('', mountain_list, name='mountain_list'),
    path('<int:pk>/', MountainDetailView.as_view(), name='mountain_detail'),

    path('<int:mountain_pk>/get_weather_forecast/', get_weather_forecast, name='get_weather_forecast'),
    path('<int:mountain_pk>/get_air/', get_air, name='get_air'),
    path('<int:mountain_pk>/get_news/', get_news, name='get_news'),

    path('<int:mountain_pk>/likes/', mountain_likes, name='mountain_likes'),
    path('<int:mountain_pk>/courses/', CourseListView.as_view(), name='course_list'),
    path('<int:mountain_pk>/courses/<int:course_pk>/bookmark/', bookmark, name='bookmark'),
    path('<int:mountain_pk>/courses/<int:course_pk>/download/', gpxDownloadView.as_view(), name='download'),

    path('courses/', course_all_list, name='course_all_list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),

    path('<int:pk>/review/', create_review, name='create_review'),
    path('<int:pk>/review/<int:review_pk>/update/', review_update, name='review_update'),
    path('<int:pk>/review/<int:review_pk>/delete/', review_delete, name='review_delete'),
    path('<int:pk>/review/<int:review_pk>/delete/image/', review_image_delete, name='review_image_delete'),
    path('<int:pk>/review/<int:review_pk>/likes/', review_likes, name='review_likes'),
    
    path('weather_forecast/<int:pk>/', weather_forecast, name='weather_forecast'),
]
