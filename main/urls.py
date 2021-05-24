from django.urls import path
from .views import MainPage

app_name = 'main'

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
]
