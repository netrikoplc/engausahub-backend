from django.urls import path, include
from .views import ContactViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("contacts/send", ContactViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
