from django.shortcuts import render
from django.views.generic import ListView
from eshop.models import Course

# Create your views here.


class MainPage(ListView):
    template_name = 'main/index.html'

    def get_queryset(self):
        return Course.objects.filter(active=True)
