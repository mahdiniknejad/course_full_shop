from django.urls import path
from .views import (
    MainPage,
    DetailPage,
    VideoViewPage,
    CategoryViewPage,
    DashboardView,
)

app_name = 'main'

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('course/<str:slug>/', DetailPage.as_view(), name='detail'),
    path('course/<str:slug>/<int:file_id>/', VideoViewPage.as_view(), name='video_view'),
    path('category/<str:slug>/', CategoryViewPage.as_view(), name='category'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
