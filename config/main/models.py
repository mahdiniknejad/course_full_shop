from django.db import models
from django.contrib.auth import get_user_model
from eshop.models import Course
from django.utils import timezone
from jalali_date import datetime2jalali

# Create your models here.

User = get_user_model()


class Cart(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name="خریدار"
    )
    is_paid = models.BooleanField(
        default=False, verbose_name="آیا پرداخت شده؟")
    price = models.PositiveIntegerField(default=0, verbose_name="مبلغ")
    _time = models.DateTimeField(default=None, null=True) 

    def __str__(self):
        return self.owner.get_full_name()

    def paid(self):
        self.time = timezone.now()
        self.is_paid = True
        self.save()

    def jalali_paid_time(self):
        return f"{datetime2jalali(self._time).strftime('%Y/%m/%d') }"

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد های خرید"


class SubCart(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="دوره آموزشی"
    )
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, verbose_name="سبد خرید")

    def __str__(self):
        return self.course.title

    class Meta:
        verbose_name = "دوره خریداری شده"
        verbose_name_plural = "دوره های خریداری شده"
