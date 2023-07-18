from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course, Enrollment
from students.models import Student


User = get_user_model()


class CourseTransaction(models.Model):
    enrollment = models.ForeignKey(Enrollment, blank=False, on_delete=models.CASCADE, related_name="course_transaction")
    reference = models.CharField(max_length=100, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.enrollment.student} - {self.enrollment.course_of_study.title}"

    class Meta:
        verbose_name = "course transaction"
        verbose_name_plural = "course transactions"
        unique_together = ("enrollment", "reference", "created_at")
