from django.urls import path, include
from .views import GoogleLogin, FacebookLogin
from django.views.generic import TemplateView


urlpatterns = [
    path(
        "password/reset/confirm/<uid>/<token>/",
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path("", include("dj_rest_auth.urls")),
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path("facebook/", FacebookLogin.as_view(), name="fb_login"),
    path("registration/", include("dj_rest_auth.registration.urls")),
]
