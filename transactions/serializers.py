from rest_framework import serializers
from .models import CourseTransaction
from paystackapi.paystack import Paystack
from courses.models import Course, Enrollment
from students.models import Student
from .models import CourseTransaction
from django.conf import settings


paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)


class CourseTransactionPostSerializer(serializers.Serializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    reference = serializers.CharField(max_length=100)

    def create(self, validated_data):
        try:
            course = Course.objects.get(id=self.validated_data["course"].id)
            student = Student.objects.get(user=self.context["request"].user)
            enrollment = Enrollment.objects.get(course_of_study=course, student=student)
            enrollment.paid = True
            enrollment.save()
            course_transaction = CourseTransaction.objects.create(
                enrollment=enrollment, reference=self.validated_data["reference"]
            )
            course_transaction.save()
            return validated_data
        except (Course.DoesNotExist, Student.DoesNotExist, Enrollment.DoesNotExist):
            raise serializers.ValidationError("You are not enrolled in this course")
        # verification = paystack.transaction.verify(reference=self.validated_data["reference"])

        # try:
        #     if verification["data"]["status"] == "success" and verification["data"]["customer"]["email"] == user.email:
        #         try:
        #             course = Course.objects.get(id=self.validated_data["course"])
        #             student = Student.objects.get(user=self.context["user"].user)
        #             enrollment = Enrollment.objects.get(course_of_study == course, student=student)

        #             if (verification["data"]["amount"] / 100) == course.price:
        #                 enrollment.paid = True
        #                 enrollment.save()
        #                 course_transaction = CourseTransaction.objects.create(
        #                     course=course, student=student, reference=self.validated_data["reference"]
        #                 )
        #                 course_transaction.save()
        #                 return validated_data
        #             raise serializers.ValidationError("Amount paid does not match course price")
        #         except (Course.DoesNotExist, Student.DoesNotExist, Enrollment.DoesNotExist):
        #             raise serializers.ValidationError("You are not enrolled in this course")
        #     else:
        #         raise serializers.ValidationError("Payment verification failed")
        # except KeyError:
        #     raise serializers.ValidationError("Payment verification failed")
