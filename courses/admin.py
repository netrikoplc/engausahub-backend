from django.contrib import admin
from .models import Course, Enrollment, Graduate


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "duration")
    search_fields = ("title", "price", "duration")
    readonly_fields = ("slug",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Personal Information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "gender",
                    "date_of_birth",
                    "image",
                ),
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "phone_number",
                    "email",
                    "street_address",
                    "city",
                    "state",
                    "country",
                )
            },
        ),
        (
            "Guardian Information",
            {
                "fields": (
                    "guardian_first_name",
                    "guardian_last_name",
                    "guardian_phone_number",
                    "guardian_email",
                    "guardian_address",
                    "guardian_relationship",
                )
            },
        ),
        (
            "Course Information",
            {
                "fields": (
                    "course_of_study",
                    "session",
                    "learning_center",
                    "student",
                    "paid",
                    "scholarship",
                    "enrolled_on",
                )
            },
        ),
    )
    list_display = (
        "student",
        "first_name",
        "last_name",
        "course_of_study",
        "learning_center",
        "session",
        "paid",
        "scholarship",
        "enrolled_on",
    )
    search_fields = (
        "first_name",
        "last_name",
        "course",
        "student",
    )
    readonly_fields = ("enrolled_on",)
    ordering = ("-enrolled_on",)


@admin.register(Graduate)
class GraduateAdmin(admin.ModelAdmin):
    list_display = ("names", "registration_number")
    search_fields = ("names", "registration_number")
