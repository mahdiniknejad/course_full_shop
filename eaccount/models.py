from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class EditedUser(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='نام'
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='نام خانوادگی'
    )
    email = models.EmailField(
        blank=False,
        null=False,
        unique=True,
        verbose_name='آدرس ایمیل',
        help_text="ایمیل شما نباید در سامانه موجود باشد"
    )
    number = models.CharField(
        max_length=12,
        verbose_name='شماره تلفون',
        blank=False,
        null=False,
        help_text="شماره تلفون خود را با دقت وارد نمایید"
    )
