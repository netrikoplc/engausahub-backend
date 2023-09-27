"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    # local apps
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("courses.urls")),
    path("", include("students.urls")),
    path("", include("transactions.urls"), name="transactions"),
    path("", include("blog.urls"), name="blog"),
    path("", include("contacts.urls"), name="contacts"),
    path("", include("info.urls"), name="info"),
    path(
        "auth/password-reset/new/<uid>/<token>/",
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    # third-party apps
    path("__reload__/", include("django_browser_reload.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
]
