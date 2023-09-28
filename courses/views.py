from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from .models import Course, Enrollment, Graduate
from .serializers import CourseSerializer, EnrollmentPostSerializer, EnrollmentGetSerializer, GraduateGetSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from utils.mixins import SerializerByMethodMixin
from .permissions import IsEnrollmentRetrieve
from students.models import Student
from rest_framework.response import Response
from rest_framework import status


class CourseViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


class EnrollmentViewSet(SerializerByMethodMixin, GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin):
    queryset = Enrollment.objects.all()
    serializer_map = {
        "GET": EnrollmentGetSerializer,
        "POST": EnrollmentPostSerializer,
    }

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        return self.queryset.filter(student=student)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "retrieve":
            self.permission_classes = [IsEnrollmentRetrieve]
        return super().get_permissions()


class GraduateViewSet(GenericViewSet, RetrieveModelMixin):
    queryset = Graduate.objects.all()
    serializer_class = GraduateGetSerializer
    permission_classes = [AllowAny]
    lookup_field = "registration_number"

    def retrieve(self, request, *args, **kwargs):
        registration_number = self.kwargs["registration_number"].replace("-", "/")

        print(registration_number)

        try:
            graduate = self.queryset.get(registration_number=registration_number)
        except Graduate.DoesNotExist:
            return Response("No graduate found", status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(graduate)
        return Response(serializer.data)
