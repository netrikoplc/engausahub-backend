from django.test import TestCase
from courses.models import Course, Enrollment
from students.models import Student
from django.contrib.auth import get_user_model


class CourseModelTest(TestCase):
    """Test course model"""

    def setUp(self):
        """Setup test variables"""
        self.course = Course.objects.create(title="building installation skills", price=30_000, duration=6)

    def test_course_model(self):
        """Test course model"""
        self.assertIsInstance(self.course, Course)
        self.assertEqual(self.course.title, "building installation skills")
        self.assertEqual(self.course.price, 30_000)
        self.assertEqual(self.course.duration, 6)
        self.assertEqual(self.course.slug, "building-installation-skills")
        self.assertEqual(str(self.course), "building installation skills")

    def test_course_model_verbose_name(self):
        """Test course model verbose name"""
        self.assertEqual(str(Course._meta.verbose_name), "course")
        self.assertEqual(str(Course._meta.verbose_name_plural), "courses")


class EnrollmentModelTest(TestCase):
    """Test enrollment model"""

    def setUp(self):
        """Setup test variables"""
        self.course_of_study = Course.objects.create(title="building installation skills", price=30_000, duration=6)
        self.user = get_user_model().objects.create_user(
            first_name="Hussaini", last_name="Usman", email="test@example.com"
        )
        self.student = Student.objects.create(user=self.user)
        self.data = {
            "first_name": "Hussaini",
            "last_name": "Usman",
            "street_address": "No 1, Kano Road",
            "city": "Yola",
            "state": "Adamawa",
            "country": "Nigeria",
            "email": "test@example.com",
            "phone_number": "+2347030000000",
            "gender": "male",
            "date_of_birth": "1990-01-01",
            "image": "https://res.cloudinary.com/netriko/image/upload/v1/engausahub/uploads/enrollment/Hussaini_Usman-906496d5-1aca-4664-b627-edfbe64eaffa_gqnxcm",
            "guardian_first_name": "Usman",
            "guardian_last_name": "Maina",
            "guardian_phone_number": "+2347030000001",
            "guardian_relationship": "Father",
            "guardian_address": "No 1, Kano Road, Yola, Adamawa State, Nigeria",
            "highest_qualification": "BSc",
            "school_attended": "University of Maiduguri",
            "course_of_study": self.course_of_study,
            "session": "03/2021",
            "learning_center": "farm center",
            "student": self.student,
            "paid": True,
            "scholarship": False,
            "enrolled_on": "2023-07-15T17:54:43.755470Z",
        }

        self.enrollment = Enrollment.objects.create(
            first_name=self.data["first_name"],
            last_name=self.data["last_name"],
            street_address=self.data["street_address"],
            city=self.data["city"],
            state=self.data["state"],
            country=self.data["country"],
            email=self.data["email"],
            phone_number=self.data["phone_number"],
            gender=self.data["gender"],
            date_of_birth=self.data["date_of_birth"],
            image=self.data["image"],
            guardian_first_name=self.data["guardian_first_name"],
            guardian_last_name=self.data["guardian_last_name"],
            guardian_phone_number=self.data["guardian_phone_number"],
            guardian_relationship=self.data["guardian_relationship"],
            guardian_address=self.data["guardian_address"],
            highest_qualification=self.data["highest_qualification"],
            school_attended=self.data["school_attended"],
            course_of_study=self.data["course_of_study"],
            session=self.data["session"],
            learning_center=self.data["learning_center"],
            student=self.data["student"],
            paid=self.data["paid"],
            scholarship=self.data["scholarship"],
            enrolled_on=self.data["enrolled_on"],
        )

    def test_enrollment_model(self):
        """Test enrollment model"""
        self.assertIsInstance(self.enrollment, Enrollment)
        self.assertEqual(self.enrollment.first_name, self.data["first_name"])
        self.assertEqual(self.enrollment.last_name, self.data["last_name"])
        self.assertEqual(self.enrollment.street_address, self.data["street_address"])
        self.assertEqual(self.enrollment.city, self.data["city"])
        self.assertEqual(self.enrollment.state, self.data["state"])
        self.assertEqual(self.enrollment.country, self.data["country"])
        self.assertEqual(self.enrollment.email, self.data["email"])
        self.assertEqual(self.enrollment.phone_number, self.data["phone_number"])
        self.assertEqual(self.enrollment.gender, self.data["gender"])
        self.assertEqual(self.enrollment.date_of_birth, self.data["date_of_birth"])
        self.assertEqual(self.enrollment.image, self.data["image"])
        self.assertEqual(self.enrollment.guardian_first_name, self.data["guardian_first_name"])
        self.assertEqual(self.enrollment.guardian_last_name, self.data["guardian_last_name"])
        self.assertEqual(self.enrollment.guardian_phone_number, self.data["guardian_phone_number"])
        self.assertEqual(self.enrollment.guardian_relationship, self.data["guardian_relationship"])
        self.assertEqual(self.enrollment.guardian_address, self.data["guardian_address"])
        self.assertEqual(self.enrollment.highest_qualification, self.data["highest_qualification"])
        self.assertEqual(self.enrollment.school_attended, self.data["school_attended"])
        self.assertEqual(self.enrollment.course_of_study, self.data["course_of_study"])
        self.assertEqual(self.enrollment.session, self.data["session"])
        self.assertEqual(self.enrollment.learning_center, self.data["learning_center"])
        self.assertEqual(self.enrollment.student, self.data["student"])
        self.assertTrue(self.enrollment.paid)
        self.assertFalse(self.enrollment.scholarship)
        self.assertEqual(self.enrollment.enrolled_on, self.data["enrolled_on"])
        self.assertEqual(str(self.enrollment), "Hussaini Usman - building installation skills")
        self.assertEqual(str(Enrollment._meta.verbose_name), "enrollment")
        self.assertEqual(str(Enrollment._meta.verbose_name_plural), "enrollments")
        self.assertEqual(Enrollment._meta.unique_together, (("course_of_study", "student"),))
