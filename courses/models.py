from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from students.models import Student
from phonenumber_field.modelfields import PhoneNumberField
from django_resized import ResizedImageField
import uuid
import os


User = get_user_model()


def make_enrollment_image_file_path(instance, filename):
    """Generate file path for new profile image"""
    ext = filename.split(".")[-1]
    filename = f"{instance.student.user.first_name}_{instance.student.user.last_name}-{uuid.uuid4()}.{ext}"
    return os.path.join("uploads/enrollment/", filename)


class Course(models.Model):
    title = models.CharField(max_length=150, blank=False, null=False, unique=True)
    price = models.IntegerField(blank=False, null=False)
    duration = models.IntegerField(blank=False, null=False)
    slug = models.SlugField(max_length=150, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "course"
        verbose_name_plural = "courses"


class Enrollment(models.Model):
    GENDERS = (("male", "Male"), ("female", "Female"))
    LEARNING_CENTERS = (
        ("farm center", "Farm Center"),
        ("rijiyar zaki", "Rijiya Zaki"),
    )
    SESSIONS = (
        ("Weekdays (Morning)", "Weekdays (Morning)"),
        ("Weekdays (Afternoon)", "Weekdays (Afternoon)"),
        ("Weekends", "Weekends"),
    )
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    street_address = models.CharField(max_length=256, blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=50, blank=False, null=False)
    country = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(max_length=256, blank=False, null=False)
    phone_number = PhoneNumberField(blank=False, null=False)
    gender = models.CharField(choices=GENDERS, max_length=6, blank=False, null=False)
    date_of_birth = models.DateField(blank=False, null=False)
    image = ResizedImageField(
        upload_to=make_enrollment_image_file_path,
        size=[400, 400],
        quality=-1,
        scale=0.5,
        crop=["middle", "center"],
        null=True,
        blank=True,
    )

    guardian_first_name = models.CharField(max_length=50, blank=False, null=False)
    guardian_last_name = models.CharField(max_length=50, blank=False, null=False)
    guardian_phone_number = PhoneNumberField(blank=False, null=False)
    guardian_email = models.EmailField(max_length=256, blank=False, null=False)
    guardian_relationship = models.CharField(max_length=50, blank=False, null=False)
    guardian_address = models.CharField(max_length=256, blank=False, null=False)

    highest_qualification = models.CharField(max_length=50, blank=True, null=True)
    school_attended = models.CharField(max_length=50, blank=True, null=True)

    course_of_study = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name="enrollment_course")
    session = models.CharField(choices=SESSIONS, max_length=50, blank=False, null=False)
    learning_center = models.CharField(choices=LEARNING_CENTERS, max_length=50, blank=False, null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name="enrollments")
    graduate = models.BooleanField(default=False, blank=False, null=False)
    registration_number = models.CharField(max_length=50, blank=True, null=True)
    paid = models.BooleanField(default=False, blank=False, null=False)
    scholarship = models.BooleanField(default=False, blank=False, null=False)
    enrolled_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course_of_study.title}"

    class Meta:
        verbose_name = "enrollment"
        verbose_name_plural = "enrollments"
        unique_together = ("course_of_study", "student")


class Graduate(models.Model):
    GENDERS = (("male", "Male"), ("female", "Female"))

    names = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.CharField(max_length=20, blank=True, null=True)

    phone_number = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)

    guardian_email = models.CharField(max_length=256, blank=True, null=True)
    guardian_full_name = models.CharField(max_length=50, blank=True, null=True)
    guardian_occupation = models.CharField(max_length=50, blank=True, null=True)
    guardian_phone = models.CharField(max_length=50, blank=True, null=True)

    primary_school = models.CharField(max_length=50, blank=True, null=True)
    secondary_school = models.CharField(max_length=50, blank=True, null=True)

    registration_number = models.CharField(max_length=50, blank=True, null=True)
    session = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.names} - {self.registration_number}"

    class Meta:
        verbose_name = "graduate"
        verbose_name_plural = "graduates"
