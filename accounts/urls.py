from django.urls import path, include
from .views import GoogleLogin, FacebookLogin, CustomLoginView


urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path("facebook/", FacebookLogin.as_view(), name="fb_login"),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("login/new/", CustomLoginView.as_view(), name="login_view"),
]
