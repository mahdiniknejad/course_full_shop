from django.urls import path
from .views import test

app_name = 'main'

urlpatterns = [
    path('', test, name='main'),
]
