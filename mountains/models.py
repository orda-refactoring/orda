# from django.db import models
from .models import *
from django.conf import settings
from django.db.models import Count
from django.contrib.gis.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from math import radians, sin, cos, sqrt, atan2

# Create your models here.
class Mountain(models.Model):

    def image_path(instance, filename):
        return f'mountains/{instance.name}/{filename}'
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50 , unique=True)
    subname = models.CharField(max_length=200)
    info = models.TextField(db_column='mntn_info')
    height = models.IntegerField()
    region = models.CharField(max_length=100)
    geom = models.GeometryField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_mountains', db_table='mountains_mountain_likes')
    views = models.PositiveIntegerField(default=0)
    emndn_name = models.TextField(db_column='emndn_nm')
    
    class Meta:
        managed = False
        db_table = 'mountains_mountain'
        ordering = ['name']

    def haversine(self, lat1, lon1, lat2, lon2):
        # 위도와 경도를 도(degree)에서 라디안(radian)으로 변환
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine 공식 적용
        d_lat = lat2 - lat1
        d_lon = lon2 - lon1
        a = sin(d_lat/2)**2 + cos(lat1) * cos(lat2) * sin(d_lon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        radius = 6371  # 지구의 반지름 (단위: km)
        distance = radius * c

        return round(distance, 2)
    
    def current_location(self, user_latitude, user_longitude):
        if user_latitude is not None and user_longitude is not None:
            mountain_latitude = self.geom.y
            mountain_longitude = self.geom.x

            distance = self.haversine(user_latitude, user_longitude, mountain_latitude, mountain_longitude)
            return distance

        # 유저의 위치 정보가 없는 경우 None이나 다른 적절한 값을 반환합니다.
        return None
    
    @property
    def reviews_count(self):
        return self.review_set.count()    
    
    @property
    def top_tags(self):
        tags = self.review_set.values('tags__name').annotate(tag_count=Count('tags__name')).order_by('-tag_count')[:3]
        return [tag['tags__name'] for tag in tags]
    
    @property
    def top_tags_pk(self):
        tags = self.review_set.values('tags__pk').annotate(tag_count=Count('tags__pk')).order_by('-tag_count')[:3]
        return [tag['tags__pk'] for tag in tags]
    

    def __str__(self):
        return self.name
        

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    mntn_name = models.ForeignKey(Mountain, on_delete=models.CASCADE, to_field="name", db_column="mntn_name")
    crs_name = models.CharField(max_length=100)
    crs_name_detail = models.CharField(max_length=255, unique=True)
    distance = models.FloatField(db_column='total_distance_km')
    duration = models.CharField(max_length = 255, db_column='total_interval')
    hidden_time = models.FloatField(db_column='total_time')
    diff = models.CharField(max_length=30)
    geom = models.GeometryField()
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL,  related_name='bookmarks',  db_table='mountains_course_bookmarks')

    class Meta:
        managed = False
        db_table = 'mountains_course'
        ordering = ['id']

    def __str__(self):
        return self.crs_name_detail
    

class CourseDetail(models.Model):
    id = models.AutoField(primary_key=True)
    crs_name = models.CharField(max_length=100)  
    crs_name_detail = models.ForeignKey(Course, on_delete=models.CASCADE, to_field="crs_name_detail", db_column="crs_name_detail")  
    waypoint_name = models.CharField(max_length=50)
    waypoint_category = models.CharField(max_length=256, db_column='category')
    geom = models.GeometryField()

    class Meta:
        managed = False
        db_table = 'mountains_coursedetail'
        ordering = ['crs_name_detail']

    def __str__(self):
        return str(self.crs_name_detail)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    # category = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    def image_path(instance, filename):
        return f'reviews/{instance.mountain.name}/{filename}'
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user_id')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='reviews')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')
    image = ProcessedImageField(upload_to=image_path,
                                        processors=[ResizeToFill(500,500)],
                                        format='JPEG',
                                        options={'quality': 90},
                                        null=True,
                                        blank=True)

    class Meta:
        db_table = 'mountains_review'

    def __str__(self):
        return self.content
