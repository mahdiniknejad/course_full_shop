from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm


# Create your models here.

class EditedUser(AbstractUser):

    GENDER_CHOICES = (
        ('m', 'آقا'),
        ('f', 'خانم'),
    )
    username = models.CharField(
        max_length=150,
        unique=False,
        help_text='در صورت تمایل برای خود نام کاربری قرار دهید',
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
        unique=True,
        help_text="شماره تلفون خود را با دقت وارد نمایید"
    )
    gender = models.CharField(
        max_length=1,
        verbose_name='جنسیت',
        null=True,
        blank=True,
        choices=GENDER_CHOICES,
    )
    birth = models.DateField(
        verbose_name='تاریخ تولد',
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'number')
