from django.urls import path
from .views import course, category
app_name = 'api'

urlpatterns = [
    path('course/', course),
    path('category/course/', category, name="category"),
]

