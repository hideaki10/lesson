from django.db import models

# Create your models here.

from apps.users.models import BaseModel


class City(BaseModel):
    name = models.CharField(verbose_name="都市", max_length=20)
    desc = models.CharField(verbose_name="紹介", max_length=200)

    class Meta:
        verbose_name = "都市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(BaseModel):
    name = models.CharField(verbose_name="機構名称", max_length=50)
    desc = models.TextField(verbose_name="説明")
    tag = models.CharField(verbose_name="機構タグ", max_length=10, default="全国有名")
    category = models.CharField(verbose_name="機構種別", max_length=4, default="pxjg",
                                choices=(("pxjg", "学校"), ("gr", "個人"), ("gx", "高校")))
    click_nums = models.IntegerField(verbose_name="クリック数", default=0)
    fav_nums = models.IntegerField(verbose_name="ブックマーク", default=0)
    image = models.ImageField(verbose_name="ログ", upload_to="org/%Y/%m", max_length=100, default="default.jpg")
    address = models.CharField(verbose_name="住所", max_length=100, default="")
    students = models.IntegerField(verbose_name="人数", default=0)
    course_nums = models.IntegerField(verbose_name="コース数", default=0)

    is_auth = models.BooleanField(verbose_name="認証", default=False)
    is_glod = models.BooleanField(verbose_name="ゴールド", default=False)

    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def courses(self):
        # courses = Course.objects.filter(course_org=self)

        courses = self.course_set.filter(is_classics=True)[:3]
        return courses

    class Meta:
        verbose_name = "機構"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(BaseModel):
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="機構名称")
    name = models.CharField(verbose_name="氏名", max_length=50)
    work_years = models.IntegerField(verbose_name="仕事年数", default=0)
    work_company = models.CharField(verbose_name="会社", max_length=50)
    work_position = models.CharField(verbose_name="職位", max_length=50)
    points = models.CharField(verbose_name="特徴", max_length=50)
    click_nums = models.IntegerField(verbose_name="クリック数", default=0)
    fav_nums = models.IntegerField(verbose_name="ブックマーク", default=0)
    age = models.IntegerField(verbose_name="年齢", default=18)
    image = models.ImageField(verbose_name="アイコン", upload_to="teacher/%Y/%m", max_length=100)

    class Meta:
        verbose_name = "講師"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def course_nums(self):
        return self.course_set.all()

