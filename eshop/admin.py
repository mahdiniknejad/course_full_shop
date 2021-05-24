from django.contrib import admin
from .models import Course


# Register your models here.


class CourseAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'teacher', 'thumbnail', 'price', 'publish', 'active', 'status')
    list_filter = ('title', 'teacher')
    list_per_page = 10
    ordering = ('-publish',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Course, CourseAdmin)
