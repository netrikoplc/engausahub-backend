from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestimonialViewSet, FAQViewSet

router = DefaultRouter()

router.register("testimonials", TestimonialViewSet)
router.register("faqs", FAQViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
