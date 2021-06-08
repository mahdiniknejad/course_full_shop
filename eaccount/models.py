from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class EditedUser(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True, verbose_name='آدرس ایمیل')
    number = models.CharField(max_length=12, verbose_name='شماره تلفون')