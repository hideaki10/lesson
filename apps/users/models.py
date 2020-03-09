from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

GENDER_CHOICES = (
    ("male", "男の子"),
    ("female", "女の子")
)


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='ニックネーム', default="")
    birthday = models.DateField(verbose_name="誕生日", null=True, blank=True)
    gender = models.CharField(verbose_name="性別", choices=GENDER_CHOICES, max_length=6)
    address = models.CharField(verbose_name="住所", max_length=100, default="")
    mobile = models.CharField(verbose_name="電話番号", max_length=11)
    image = models.ImageField(verbose_name="アイコン", upload_to="head_image/%Y/%m", default="default.jpg")

    class Meta:
        verbose_name = "ユーザーの情報"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username


class BaseModel(models.Model):
    add_time = models.DateField(verbose_name="挿入時間", default=datetime.now)  # nowメソッドを使わない、　

    class Meta:
        abstract = True
