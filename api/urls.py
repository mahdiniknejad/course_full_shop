from django.urls import path
from rest_framework import routers
from .views import (
    CourseViewSet,
)

app_name = 'api'

router = routers.SimpleRouter()
router.register('course', CourseViewSet, basename='course')
urlpatterns = [
]

urlpatterns += router.urls
