from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=150, blank=False)
    subject = models.CharField(max_length=256, blank=False)
    message = models.TextField(max_length=256, blank=False)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "contact"
        verbose_name_plural = "contacts"
