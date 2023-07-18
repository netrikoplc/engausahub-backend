from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from .serializers import StudentGetSerializer
from .permissions import IsStudentRetrieve
from .models import Student
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from utils.mixins import SerializerByMethodMixin
from rest_framework.permissions import IsAdminUser


class StudentViewSet(SerializerByMethodMixin, GenericViewSet, RetrieveModelMixin, ListModelMixin):
    queryset = Student.objects.all()
    serializer_map = {
        "GET": StudentGetSerializer,
    }

    def get_instance(self):
        try:
            student = Student.objects.get(user=self.request.user)
        except Student.DoesNotExist:
            raise NotFound("No student record found for the logged-in user.")
        return student

    def get_permissions(self):
        if self.action == "me":
            self.permission_classes = [IsStudentRetrieve]
        elif self.action == "list":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    @action(detail=False, methods=["get"])
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
