from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField


User = get_user_model()


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="student")

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "student"
        verbose_name_plural = "students"
