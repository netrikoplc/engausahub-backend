from .views import CourseTransactionViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("transactions", CourseTransactionViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
