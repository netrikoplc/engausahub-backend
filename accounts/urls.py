from django.urls import path, include
from .views import GoogleLogin, FacebookLogin


urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path("facebook/", FacebookLogin.as_view(), name="fb_login"),
    path("registration/", include("dj_rest_auth.registration.urls")),
]
