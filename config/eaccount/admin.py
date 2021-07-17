from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from jalali_date.admin import ModelAdminJalaliMixin 


# Register your models here.
User = get_user_model()


class UserAdmin(ModelAdminJalaliMixin, BaseUserAdmin):
	pass

UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'number')
UserAdmin.fieldsets[1][1]['fields'] = ('first_name', 'last_name', 'email', 'number', 'gender', 'birth',)

admin.site.register(User, UserAdmin)
