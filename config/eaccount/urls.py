from django.urls import path
from .views import (
	EditedLoginView,
	EditedLogoutView,
	RegisterView,
	ActivateAccount,
	EditedPasswordResetView,
	EditedPasswordResetDoneView,
	EditedPasswordResetConfirmView,
	EditedPasswordResetCompleteView,
)


app_name = 'account'

urlpatterns = [
    path('login/', EditedLoginView.as_view(), name='login'),
    path('logout/', EditedLogoutView.as_view(), name='logout'),
    path('register/', RegisterView, name='register'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

    # change password
    path('password/reset/', EditedPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', EditedPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/', EditedPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', EditedPasswordResetCompleteView.as_view(), name='password_reset_comlete'),
]
