from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from jalali_date import datetime2jalali
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

class OffCourse(models.Model):
    event = models.CharField(max_length=244, null=True, verbose_name='مناسبت تخفیف')
    expire = models.DateTimeField(verbose_name='تاریخ اتمام تخفیف')
    percent = models.IntegerField(default=5, verbose_name='تخفیف (درصد)')
    active = models.BooleanField(default=True, verbose_name="آیا 'تخفیف' فعال است ؟")

    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیفات'

    def __str__(self):
        return "{event} -  {percent}%  -  {date}".format(event=self.event, percent=self.percent,
                                                         date=datetime2jalali(self.expire).strftime('%Y/%m/%d'))

    def is_active(self):
        if self.expire < timezone.now():
            self.active = False
            self.save()
            return False
        elif not self.active:
            return False
        return True

    is_active.boolean = True

    def get_expire_time(self):
        return "{}/{}/{}".format(self.expire.year, self.expire.month, self.expire.day)

    # def save(self, *args, **kwargs):
    #     if self.active:
    #         self.active = False
    #         for course_off in OffCourse.objects.all():
    #             if course_off.active:
    #                 course_off.active = False
    #                 course_off.save()
    #         self.active = True
    #     super(OffCourse, self).save(*args, **kwargs)

def pre_save_signals_callback(sender, **kwargs):
    obj = kwargs.get('instance')
    if obj.active:
        for course_off in OffCourse.objects.all():
            if course_off.active:
                course_off.active = False
                course_off.save()
        obj.active = True

pre_save.connect(pre_save_signals_callback, sender=OffCourse)

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
    thumbnail = models.ImageField(upload_to=make_random_name, verbose_name='تصویر دوره 600 * 600')
    category = models.ManyToManyField('Category', related_name='courses', verbose_name='دسته بندی')
    description = models.TextField(verbose_name='شرح دوره')
    price = models.IntegerField(verbose_name='قیمت دوره', null=False, blank=False,
                                help_text='قیمت را به "تومان" وارد کنید')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار دوره')
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, verbose_name="آیا دوره فعال است ؟")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت دوره")

    class Meta:
        verbose_name = 'دوره آموزشی'
        verbose_name_plural = 'دورهای آموزشی'

    def __str__(self):
        return self.title

    def convert_image_url_to_html(self):
        return format_html('<img src="{url}" width="{width}" />'.format(url=self.thumbnail.url, width='50px'))

    convert_image_url_to_html.short_description = 'تصویر'

    def convert_category_to_str(self):
        return " - ".join([category.title for category in self.category.filter(active=True)])

    def value_with_off(self):
        event = OffCourse.objects.get(active=True)
        return int(self.price - (event.percent / 100 * self.price))


class UploadFile(models.Model):
    title = models.CharField(max_length=244, null=False, default='', verbose_name='فایل آموزشی')
    file = models.FileField(upload_to=make_random_name, verbose_name='فایل')
    course = models.ForeignKey('Course', on_delete=models.DO_NOTHING, related_name='files', null=True, blank=True,
                               verbose_name='دوره مربوط')
    free = models.BooleanField(default=False, verbose_name='آیا این فایل رایگان است؟')

    class Meta:
        verbose_name = 'فایل آموزشی'
        verbose_name_plural = 'فایل های آموزشی'

    def __str__(self):
        return self.title

    def split_upload_file_name(self):
        filename = self.file.url
        return filename.split('/')[-1]

    split_upload_file_name.short_description = 'نام فایل'


class Category(models.Model):
    title = models.CharField(max_length=244, null=False, default='', verbose_name='دسته')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='دامنه', allow_unicode=True)
    active = models.BooleanField(default=True, verbose_name="آیا 'دسته' فعال است ؟")
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='دسته والد',
                               related_name='children')

    class Meta:
        verbose_name = 'دسته'
        verbose_name_plural = 'دسته ها'
        ordering = ['-active']

    def __str__(self):
        return self.title


class Slider(models.Model):
    title = models.CharField(max_length=244, null=False, default='', verbose_name='دوره آموزشی')
    banner = models.CharField(max_length=244, null=True, blank=True, verbose_name='شعار')
    thumbnail = models.ImageField(upload_to=make_random_name, verbose_name='تصویر اسلایدر1920 * 900')
    description = models.TextField(verbose_name='شرح کوتاه برای اسلایدر')
    link = models.URLField(verbose_name='لینک دوره', default='')
    active = models.BooleanField(default=True, verbose_name="آیا 'اسلایدر' فعال است ؟")
    price = models.IntegerField(verbose_name='قیمت دوره', null=False, blank=False, default=0,
                                help_text='قیمت را به "تومان" وارد کنید')
    color = models.CharField(max_length=10, null=False, default='', verbose_name='رنگ')

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر ها'

    def __str__(self):
        return self.title
