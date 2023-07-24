from django.db import models
from django_resized import ResizedImageField
import os


def make_testimonial_image_file_path(instance, filename):
    """Generate file path for new testimonial image"""
    ext = filename.split(".")[-1]
    filename = f"{instance.name}.{ext}"
    return os.path.join("uploads/testimonial/", filename)


class Testimonials(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    job_title = models.CharField(max_length=50, blank=False, null=False)
    # image = ResizedImageField(
    #     upload_to=make_testimonial_image_file_path,
    #     size=[400, 400],
    #     quality=-1,
    #     scale=0.5,
    #     crop=["middle", "center"],
    #     null=True,
    #     blank=True,
    # )
    image = models.URLField(blank=True, null=True)
    testimonial = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "testimonial"
        verbose_name_plural = "testimonials"


class FAQs(models.Model):
    question_en = models.CharField(max_length=250, blank=False, null=False)
    question_ha = models.CharField(max_length=250, blank=False, null=False)
    answer_en = models.CharField(max_length=250, blank=False, null=False)
    answer_ha = models.CharField(max_length=250, blank=False, null=False)

    def __str__(self):
        return self.question_en

    class Meta:
        verbose_name = "faq"
        verbose_name_plural = "faqs"
