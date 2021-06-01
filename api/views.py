from rest_framework.response import Response
from rest_framework.decorators import api_view
from eshop.models import Course, Category
from .serializers import CourseSerializer, CategorySerializer


@api_view(['GET'])
def course(request):
    data = Course.objects.all()
    serialized_data = CourseSerializer(data, many=True)
    return Response(serialized_data.data)


@api_view(['GET'])
def category(request):
    course = Course.objects.last()
    data = course.category.all()
    serialized_data = CategorySerializer(data, many=True)
    return Response(serialized_data.data)
