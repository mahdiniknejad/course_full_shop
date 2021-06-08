from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .permissions import IsStaffOrReadOnly
from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from eshop.models import Course
from .serializers import (
    CourseSerializer,
    CreateCourseSerializer,
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)


class CourseViewSet(ViewSet):
    permission_classes = [IsStaffOrReadOnly, ]
    authentication_classes = [JWTCookieAuthentication, ]

    def list(self, request):
        data = Course.objects.filter(active=True)
        ser_data = CourseSerializer(data, many=True)
        return Response(ser_data.data, status=HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            data = Course.objects.get(active=True, pk=pk)
            ser_data = CourseSerializer(data)
            return Response(ser_data.data, status=HTTP_200_OK)
        except:
            return Response(status=HTTP_404_NOT_FOUND)

    def create(self, request):
        ser_data = CreateCourseSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response({'create': 'true'}, status=HTTP_201_CREATED)
        else:
            return Response(ser_data.errors, status=HTTP_400_BAD_REQUEST)

    # def update(self, request):
    #     ser_data = CreateCourseSerializer(data=request.data)
    #     if ser_data.is_valid():
    #         ser_data.save()
    #         return Response({'create': 'true'}, status=HTTP_201_CREATED)
    #     else:
    #         return Response(ser_data.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            data = Course.objects.get(pk=pk)
            data.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        except:
            return Response(status=HTTP_404_NOT_FOUND)
