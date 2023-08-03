from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from mountains.models import Course
from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class User(AbstractUser):
    def image_path(instance, filename):
        return f'accounts/{instance.pk}/{filename}'
    
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=256)
    nickname = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    message = models.CharField(max_length=200, blank=True)
    kakao_user_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    naver_user_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    visited_courses = models.ManyToManyField(Course, through='VisitedCourse', related_name='visitors', blank=True)
    level = models.IntegerField(default=1)
    profile_img = ProcessedImageField(upload_to=image_path,
                                        processors=[ResizeToFill(200,200)],
                                        format='JPEG',
                                        options={'quality': 90},
                                        null=True,
                                        blank=True)

    def check_notifications(self):
        unchecked_notifications = self.notifications.filter(is_checked=False)
        unchecked_notifications.update(is_checked=True)
        return unchecked_notifications
    
    def adjust_user_level(self):
        post_cnt = self.post_set.count()
        review_cnt = self.review_set.count()
        visited_course_cnt = self.visitedcourse_set.count()
        post_comment_cnt = self.postcomment_set.count()

        score = post_cnt * 30 + review_cnt * 20 + visited_course_cnt * 10 + post_comment_cnt * 5

        if score < 200:
            level = 1

        elif score < 500:
            level = 2

        elif score < 900:
            level = 3

        elif score < 1400:
            level = 4

        elif score >= 1400:
            level = 5

        self.level = level

        self.save()
    
class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


class VisitedCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    mountain_name = models.CharField(max_length=50)
    mountain_id = models.IntegerField()

    def __str__(self):
        return self.mountain_name

    def save(self, *args, **kwargs):
        self.mountain_name = self.course.mntn_name
        self.mountain_id = self.course.mntn_name.id
        super().save(*args, **kwargs)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_notification_url(self):
        if self.notification_type == '댓글' and self.post:
            return reverse('posts:detail', kwargs={'post_pk': self.post.pk})
        else:
            return reverse('accounts:profile', kwargs={'pk': self.user.pk})

    def __str__(self):
        return self.message
