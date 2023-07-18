from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentPostSerializer, EnrollmentGetSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from utils.mixins import SerializerByMethodMixin
from .permissions import IsEnrollmentRetrieve
from students.models import Student


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
