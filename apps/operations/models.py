from django.db import models

# Create your models here.

from apps.users.models import BaseModel
from apps.courses.models import Course
from django.contrib.auth import get_user_model

UserProfile = get_user_model()


class UserAsk(BaseModel):
    name = models.CharField(verbose_name="氏名", max_length=20)
    mobile = models.CharField(verbose_name="携帯", max_length=11)
    course_name = models.CharField(verbose_name="コース名", max_length=50)

    class Meta:
        verbose_name = "問合せ"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{name}_{course}({mobile})".format(name=self.name, course=self.course_name,
                                                  mobile=self.mobile)


class CourseComments(BaseModel):
    user = models.ForeignKey(UserProfile, verbose_name="ユーザー", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="コース", on_delete=models.CASCADE)
    comments = models.CharField(verbose_name="コメント", max_length=200)

    class Meta:
        verbose_name = "コメント"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comments


class UserFavorite(BaseModel):
    user = models.ForeignKey(UserProfile, verbose_name="ユーザー", on_delete=models.CASCADE)
    fav_id = models.IntegerField(verbose_name="id")
    fav_type = models.IntegerField(verbose_name="ブックマーク種類", choices=((1, "コース"),
                                                                     (2, "機構"), (3, "講師")))

    class Meta:
        verbose_name = "ブックマーク"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{user}_{id}".format(user=self.user.name, id=self.fav_id)


class UserMessage(BaseModel):
    user = models.ForeignKey(UserProfile, verbose_name="ユーザー", on_delete=models.CASCADE)
    message = models.CharField(verbose_name="メッセージ内容", max_length=200)
    has_read = models.BooleanField(verbose_name="既読", default=False)

    class Meta:
        verbose_name = "メッセージ"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


class UserCourse(BaseModel):
    user = models.ForeignKey(UserProfile, verbose_name="ユーザー", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="コース", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "ユーザーコース"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course
