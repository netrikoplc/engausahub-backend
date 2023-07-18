from django.test import TestCase
from courses.serializers import (
    CourseSerializer,
    EnrollmentGetSerializer,
    EnrollmentStudentGetSerializer,
    EnrollmentPostSerializer,
)
from courses.models import Course, Enrollment
from students.models import Student
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from collections import OrderedDict
import datetime
import os


class CourseSerializerTest(TestCase):
    def setUp(self):
        self.data = {"title": "Building Installation Skills", "price": 30_000, "duration": 6, "slug": None}

    def test_course_serializer(self):
        serializer = CourseSerializer(data=self.data)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        self.assertEqual(serializer.validated_data, self.data)
        self.assertEqual(serializer.data, self.data)
        self.assertEqual(serializer.data["title"], "Building Installation Skills")
        self.assertEqual(serializer.data["price"], 30_000)
        self.assertEqual(serializer.data["duration"], 6)
        self.assertIsNone(serializer.data["slug"])


class EnrollmentGetSerializerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            first_name="Hussaini", last_name="Usman", email="test@example.com"
        )
        serializer_directory = os.path.dirname(os.path.abspath(__file__))
        self.image_file = SimpleUploadedFile(
            name="test_image.png",
            content=open(os.path.join(serializer_directory, "test_image.png"), "rb").read(),
            content_type="image/png",
        )
        self.student = Student.objects.create(user=self.user)
        self.course = Course.objects.create(title="Building Installation Skills", price=30_000, duration=6)

        self.data = OrderedDict(
            [
                (
                    "course_of_study",
                    OrderedDict(
                        [
                            ("title", "Building Installation Skills"),
                            ("price", 30_000),
                            ("duration", 6),
                            ("slug", "building-installation-skills"),
                        ]
                    ),
                ),
                ("first_name", "Hussaini"),
                ("last_name", "Usman"),
                ("street_address", "No 1, Kano Road"),
                ("city", "Yola"),
                ("state", "Adamawa"),
                ("country", "Nigeria"),
                ("email", "test@example.com"),
                ("phone_number", "+2347030000000"),
                ("gender", "male"),
                ("date_of_birth", datetime.date(1990, 1, 1)),
                ("image", self.image_file),
                ("guardian_first_name", "Usman"),
                ("guardian_last_name", "Maina"),
                ("guardian_phone_number", "+2347030000001"),
                ("guardian_email", "guardian@example.com"),
                ("guardian_relationship", "Father"),
                ("guardian_address", "No 1, Kano Road, Yola, Adamawa State, Nigeria"),
                ("highest_qualification", "BSc"),
                ("school_attended", "University of Maiduguri"),
                ("session", "03/2021"),
                ("learning_center", "farm center"),
                ("paid", True),
                ("scholarship", False),
                ("enrolled_on", datetime.datetime(2023, 7, 16, 10, 30, 0, 0, tzinfo=datetime.timezone.utc)),
                ("student", self.student.id),
            ]
        )

    def test_enrollment_get_serializer(self):
        serializer = EnrollmentGetSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})
        self.data["date_of_birth"] = str(self.data["date_of_birth"])
        serializer.validated_data["date_of_birth"] = str(serializer.validated_data["date_of_birth"])
        self.data["enrolled_on"] = str(self.data["enrolled_on"])
        serializer.validated_data["enrolled_on"] = str(serializer.validated_data["enrolled_on"])
        serializer.validated_data["student"] = serializer.validated_data["student"].id
        self.assertEqual(serializer.validated_data, self.data)
        self.assertEqual(serializer.validated_data["first_name"], self.data["first_name"])
        self.assertEqual(serializer.validated_data["last_name"], self.data["last_name"])
        self.assertEqual(serializer.validated_data["street_address"], self.data["street_address"])
        self.assertEqual(serializer.validated_data["city"], self.data["city"])
        self.assertEqual(serializer.validated_data["state"], self.data["state"])
        self.assertEqual(serializer.validated_data["country"], self.data["country"])
        self.assertEqual(serializer.validated_data["email"], self.data["email"])
        self.assertEqual(serializer.validated_data["phone_number"], self.data["phone_number"])
        self.assertEqual(serializer.validated_data["gender"], self.data["gender"])
        self.assertEqual(serializer.validated_data["date_of_birth"], self.data["date_of_birth"])
        self.assertEqual(serializer.validated_data["image"], self.data["image"])
        self.assertEqual(serializer.validated_data["guardian_first_name"], self.data["guardian_first_name"])
        self.assertEqual(serializer.validated_data["guardian_last_name"], self.data["guardian_last_name"])
        self.assertEqual(serializer.validated_data["guardian_phone_number"], self.data["guardian_phone_number"])
        self.assertEqual(serializer.validated_data["guardian_email"], self.data["guardian_email"])
        self.assertEqual(serializer.validated_data["guardian_relationship"], self.data["guardian_relationship"])
        self.assertEqual(serializer.validated_data["guardian_address"], self.data["guardian_address"])
        self.assertEqual(serializer.validated_data["highest_qualification"], self.data["highest_qualification"])
        self.assertEqual(serializer.validated_data["school_attended"], self.data["school_attended"])
        self.assertEqual(serializer.validated_data["session"], self.data["session"])
        self.assertEqual(serializer.validated_data["learning_center"], self.data["learning_center"])
        self.assertTrue(serializer.validated_data["paid"])
        self.assertFalse(serializer.validated_data["scholarship"])
        self.assertEqual(serializer.validated_data["enrolled_on"], self.data["enrolled_on"])
        self.assertEqual(serializer.validated_data["student"], self.data["student"])


class EnrollmentStudentGetSerializerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            first_name="Hussaini", last_name="Usman", email="test@example.com"
        )
        serializer_directory = os.path.dirname(os.path.abspath(__file__))
        self.image_file = SimpleUploadedFile(
            name="test_image.png",
            content=open(os.path.join(serializer_directory, "test_image.png"), "rb").read(),
            content_type="image/png",
        )
        self.course = Course.objects.create(title="Building Installation Skills", price=30_000, duration=6)

        self.data = OrderedDict(
            [
                (
                    "course_of_study",
                    OrderedDict(
                        [
                            ("title", "Building Installation Skills"),
                            ("price", 30_000),
                            ("duration", 6),
                            ("slug", "building-installation-skills"),
                        ]
                    ),
                ),
                ("first_name", "Hussaini"),
                ("last_name", "Usman"),
                ("street_address", "No 1, Kano Road"),
                ("city", "Yola"),
                ("state", "Adamawa"),
                ("country", "Nigeria"),
                ("email", "test@example.com"),
                ("phone_number", "+2347030000000"),
                ("gender", "male"),
                ("date_of_birth", datetime.date(1990, 1, 1)),
                ("image", self.image_file),
                ("guardian_first_name", "Usman"),
                ("guardian_last_name", "Maina"),
                ("guardian_phone_number", "+2347030000001"),
                ("guardian_email", "guardian@example.com"),
                ("guardian_relationship", "Father"),
                ("guardian_address", "No 1, Kano Road, Yola, Adamawa State, Nigeria"),
                ("highest_qualification", "BSc"),
                ("school_attended", "University of Maiduguri"),
                ("session", "03/2021"),
                ("learning_center", "farm center"),
                ("paid", True),
                ("scholarship", False),
                ("enrolled_on", datetime.datetime(2023, 7, 16, 10, 30, 0, 0, tzinfo=datetime.timezone.utc)),
            ]
        )

    def test_enrollment_student_get_serializer(self):
        serializer = EnrollmentStudentGetSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})
        self.data["date_of_birth"] = str(self.data["date_of_birth"])
        serializer.validated_data["date_of_birth"] = str(serializer.validated_data["date_of_birth"])
        self.data["enrolled_on"] = str(self.data["enrolled_on"])
        serializer.validated_data["enrolled_on"] = str(serializer.validated_data["enrolled_on"])
        self.assertEqual(serializer.validated_data, self.data)
        self.assertEqual(serializer.validated_data["first_name"], self.data["first_name"])
        self.assertEqual(serializer.validated_data["last_name"], self.data["last_name"])
        self.assertEqual(serializer.validated_data["street_address"], self.data["street_address"])
        self.assertEqual(serializer.validated_data["city"], self.data["city"])
        self.assertEqual(serializer.validated_data["state"], self.data["state"])
        self.assertEqual(serializer.validated_data["country"], self.data["country"])
        self.assertEqual(serializer.validated_data["email"], self.data["email"])
        self.assertEqual(serializer.validated_data["phone_number"], self.data["phone_number"])
        self.assertEqual(serializer.validated_data["gender"], self.data["gender"])
        self.assertEqual(serializer.validated_data["date_of_birth"], self.data["date_of_birth"])
        self.assertEqual(serializer.validated_data["image"], self.data["image"])
        self.assertEqual(serializer.validated_data["guardian_first_name"], self.data["guardian_first_name"])
        self.assertEqual(serializer.validated_data["guardian_last_name"], self.data["guardian_last_name"])
        self.assertEqual(serializer.validated_data["guardian_phone_number"], self.data["guardian_phone_number"])
        self.assertEqual(serializer.validated_data["guardian_email"], self.data["guardian_email"])
        self.assertEqual(serializer.validated_data["guardian_relationship"], self.data["guardian_relationship"])
        self.assertEqual(serializer.validated_data["guardian_address"], self.data["guardian_address"])
        self.assertEqual(serializer.validated_data["highest_qualification"], self.data["highest_qualification"])
        self.assertEqual(serializer.validated_data["school_attended"], self.data["school_attended"])
        self.assertEqual(serializer.validated_data["session"], self.data["session"])
        self.assertEqual(serializer.validated_data["learning_center"], self.data["learning_center"])
        self.assertTrue(serializer.validated_data["paid"])
        self.assertFalse(serializer.validated_data["scholarship"])
        self.assertEqual(serializer.validated_data["enrolled_on"], self.data["enrolled_on"])


# class EnrollmentPostSerializerTest(TestCase):
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             first_name="Hussaini", last_name="Usman", email="
