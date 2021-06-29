from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


# Register your models here.

UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'number')
UserAdmin.fieldsets[1][1]['fields'] = ('first_name', 'last_name', 'email', 'number')

admin.site.register(get_user_model(), UserAdmin)
