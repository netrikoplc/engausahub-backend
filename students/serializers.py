from rest_framework import status
from dj_rest_auth.serializers import UserDetailsSerializer
from .models import Student
from rest_framework import serializers
from courses.models import Enrollment
from courses.serializers import EnrollmentStudentGetSerializer
from rest_framework.exceptions import NotFound, ValidationError


class StudentGetSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()
    enrollments = serializers.SerializerMethodField()

    def get_enrollments(self, obj):
        enrollments = obj.enrollments.all()
        return EnrollmentStudentGetSerializer(enrollments, many=True).data

    class Meta:
        model = Student
        fields = [
            "id",
            "user",
            "enrollments",
        ]
