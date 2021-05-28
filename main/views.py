# from django.shortcuts import render
from django.views.generic import ListView
from eshop.models import (
    Course,
    Category,
    Slider,
    OffCourse,
)


# Create your views here.


class MainPage(ListView):
    template_name = 'main/index.html'

    def get_queryset(self):
        return Course.objects.order_by('?').filter(active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(MainPage, self).get_context_data(*args, **kwargs)

        context['category_object_list'] = Category.objects.filter(active=True)
        context['new_object_list'] = Course.objects.filter(active=True).order_by('-publish')[:8]
        context['slider_object_list'] = Slider.objects.filter(active=True)[:3]
        context['discount'] = OffCourse.objects.filter(active=True)
        return context
