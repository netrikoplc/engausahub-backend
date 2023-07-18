from django.shortcuts import render
from .serializers import CourseTransactionPostSerializer
from .models import CourseTransaction
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from courses.models import Course, Enrollment
from students.models import Student


class CourseTransactionViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = CourseTransactionPostSerializer
    queryset = CourseTransaction.objects.all()
    permission_classes = [IsAuthenticated]
