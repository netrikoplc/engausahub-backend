from django.contrib import admin
from .models import Testimonials, FAQs


@admin.register(Testimonials)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "job_title")


@admin.register(FAQs)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question_en",)
