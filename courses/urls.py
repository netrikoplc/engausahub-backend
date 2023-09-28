from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, EnrollmentViewSet, GraduateViewSet

router = DefaultRouter()
router.register("courses", CourseViewSet)
router.register("enrollments", EnrollmentViewSet)
router.register("graduates", GraduateViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
