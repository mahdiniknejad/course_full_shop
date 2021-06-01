from rest_framework import serializers
from django.contrib.auth import get_user_model
from eshop.models import Category, Course


# from eshop.models import Course
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# class CourseSerializer(serializers.Serializer):
#     # category = models.ManyToManyField('Category', related_name='courses', verbose_name='دسته بندی')
#
#     title = serializers.CharField(max_length=244)
#     slug = serializers.SlugField(max_length=50, allow_unicode=True, allow_blank=False)
#     teacher = UserSerializer()
#     thumbnail = serializers.ImageField(allow_empty_file=False)
#     # category = serializers.HyperlinkedIdentityField(view_name="api:category")
#     description = serializers.CharField()
#     price = serializers.IntegerField()
#     publish = serializers.DateTimeField()
#     active = serializers.BooleanField()
#     status = serializers.CharField(max_length=1)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
