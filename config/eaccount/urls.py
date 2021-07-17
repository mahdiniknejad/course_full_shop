from django.urls import path
from .views import EditedLoginView, EditedLogoutView, RegisterView

app_name = 'account'

urlpatterns = [
	path('login/', EditedLoginView.as_view(), name='login'),
	path('logout/', EditedLogoutView.as_view(), name='logout'),
	path('register/', RegisterView, name='register'),
]