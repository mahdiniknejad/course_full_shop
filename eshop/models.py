from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid
import os


def make_random_name(instance, filename):
    end = filename.split('.')[-1]
    filename = "{name}.{end}".format(name=uuid.uuid4(), end=end)
    standard_image_ext = ['png', 'jpg', 'jpeg', 'gif', 'tif', 'tiff', 'bmp']
    if end.lower() in standard_image_ext:
        return os.path.join('upload/images', filename)
    else:
        return os.path.join('upload/files', filename)


# Create your models here.


class Course(models.Model):
    STATUS_CHOICES = (
        ('a', 'به زودی'),
        ('b', 'در حال بروزرسانی'),
        ('c', 'به اتمام رسیده'),
        ('d', 'متوقف شده'),
    )

    title = models.CharField(max_length=244, null=False, default='', verbose_name='دوره آموزشی')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='دامنه', allow_unicode=True)
    teacher = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL, related_name='course',
                                verbose_name='مدرس')
    thumbnail = models.ImageField(upload_to=make_random_name, verbose_name='تصویر دوره')
    files = models.ForeignKey('UploadFile', on_delete=models.DO_NOTHING, related_name='course', null=True, blank=True,
                              verbose_name='فایل های دوره')
    description = models.TextField(verbose_name='شرح دوره')
    price = models.IntegerField(verbose_name='قیمت دوره', null=False, blank=False,
                                help_text='قیمت را به "تومان" وارد کنید')
    publish = models.DateTimeField(default=timezone.now(), verbose_name='زمان انتشار دوره')
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, verbose_name="آیا دوره فعال است ؟")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت دوره")

    class Meta:
        verbose_name = 'دوره آموزشی'
        verbose_name_plural = 'دورهای آموزشی'

    def __str__(self):
        return self.title


class UploadFile(models.Model):
    title = models.CharField(max_length=244, null=False, default='', verbose_name='دوره آموزشی')
    file = models.FileField(upload_to=make_random_name, verbose_name='فایل')

    class Meta:
        verbose_name = 'فایل آموزشی'
        verbose_name_plural = 'فایل های آموزشی'

    def __str__(self):
        return self.title
