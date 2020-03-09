from django.db import models

from apps.users.models import BaseModel
from apps.organizations.models import Teacher
from apps.organizations.models import CourseOrg


# Create your models here.


class Course(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="機構名称")
    course_org = models.ForeignKey(CourseOrg, null=True, blank=True, on_delete=models.CASCADE, verbose_name="ゴールドレースン")
    name = models.CharField(verbose_name="コース", max_length=100)
    desc = models.CharField(verbose_name="コースの情報", max_length=300)
    learn_times = models.IntegerField(verbose_name="コースの時間", default=0)
    degree = models.CharField(verbose_name="レベル", choices=(("cj", "初心者"), ("zj", "中級"), ("gj", "高級")), max_length=3)
    students = models.IntegerField(verbose_name="人数", default=0)
    fav_nums = models.IntegerField(verbose_name="ブックマーク", default=0)
    click_nums = models.IntegerField(verbose_name="クリック数", default=0)
    category = models.CharField(verbose_name="コース種類", default="バックエンド", max_length=20)
    tag = models.CharField(verbose_name="タグ", default="", max_length=10)
    youneed_know = models.CharField(verbose_name="コース内容", default="", max_length=300)
    teacher_tell = models.CharField(verbose_name="教える", default="", max_length=300)
    is_classics = models.BooleanField(verbose_name="ゴールドコース", default=False)
    detail = models.TextField(verbose_name="コースの詳細")
    image = models.ImageField(verbose_name="コース写真", upload_to="courses/%Y/%m", max_length=100)
    notice = models.CharField(verbose_name="通知", max_length=100,default="")

    class Meta:
        verbose_name = "コース名"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def lesson_nums(self):
        return self.lesson_set.all()



class CourseTag(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="course")
    tag = models.CharField(max_length=100, verbose_name="dsa")

    class Meta:
        verbose_name = "コースタグ"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="レスーン名", max_length=100)
    learn_times = models.IntegerField(verbose_name="学習の時間", default=0)

    class Meta:
        verbose_name = "コースのレスーン"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, verbose_name="レスーン", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="ビデオ名", max_length=100)
    learn_time = models.IntegerField(verbose_name="学習の時間", default=0)
    url = models.CharField(verbose_name="url", max_length=200)

    class Meta:
        verbose_name = "ビデオ"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(BaseModel):
    course = models.ForeignKey(Course, verbose_name="コース", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="コース名", max_length=100)
    file = models.FileField(verbose_name="ダウンロード場所", upload_to="course/resource/%Y/%m", max_length=200)

    class Meta:
        verbose_name = "コースのレスーン"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
