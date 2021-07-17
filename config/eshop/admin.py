from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin
from .models import (
    Course,
    UploadFile,
    Category,
    OffCourse,
    Slider,
)


# Register your models here.


class CourseAdmin(TabularInlineJalaliMixin, admin.ModelAdmin):
    list_display = (
        '__str__', 'teacher', 'convert_image_url_to_html', 'price', 'convert_category_to_str', 'publish', 'active',
        'status')
    list_filter = ('title', 'teacher')
    search_fields = ('title', 'teacher', 'description')
    list_per_page = 10
    ordering = ('-publish',)
    prepopulated_fields = {'slug': ('title',)}


class UploadFileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'split_upload_file_name')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'active', 'parent')
    prepopulated_fields = {'slug': ('title',)}


class OffAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('__str__', 'is_active')


admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UploadFile, UploadFileAdmin)
admin.site.register(OffCourse, OffAdmin)
admin.site.register(Slider)
