from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import Student


@receiver(post_save, sender=get_user_model(), dispatch_uid="create_student")
def create_student(sender, created, **kwargs):
    user = kwargs["instance"]
    if created:
        Student.objects.create(user=user)
