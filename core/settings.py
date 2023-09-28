"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from environ import Env
from datetime import timedelta

env = Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(env_file):
    env.read_env(env_file)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "cloudinary_storage",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # local apps
    "accounts.apps.AccountsConfig",
    "courses.apps.CoursesConfig",
    "students.apps.StudentsConfig",
    "transactions.apps.TransactionsConfig",
    "blog.apps.BlogConfig",
    "contacts.apps.ContactsConfig",
    "info.apps.InfoConfig",
    # third-party apps
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "phonenumber_field",
    "ckeditor",
    "ckeditor_uploader",
    "django_browser_reload",
    "taggit",
    "dj_rest_auth",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # supported providers
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.twitter",
    "dj_rest_auth.registration",
    # "storages",
    "cloudinary",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {"default": env.db()}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_STORAGE = "cloudinary_storage.storage.StaticHashedCloudinaryStorage"

MEDIA_URL = "/engausahub/"

MEDIA_ROOT = os.path.join(BASE_DIR, "engausahub")

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

UPLOAD_ROOT = os.path.join(BASE_DIR, "engausahub", "uploads")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.CustomUser"

SITE_ID = 1


# EMAIL SETTINGS
EMAIL_BACKEND = env.str("EMAIL_BACKEND", "")

EMAIL_HOST = env.str("EMAIL_HOST")

EMAIL_PORT = env.int("EMAIL_PORT")

EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")

EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")

DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", "")


# ALLAUTH SETTINGS
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_AUTHENTICATION_METHOD = "email"

ACCOUNT_EMAIL_VERIFICATION = env.str("ACCOUNT_EMAIL_VERIFICATION")

ACCOUNT_ADAPTER = "accounts.adapter.CustomAccountAdapter"

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "offline",
        },
    },
    "facebook": {
        "METHOD": "oauth2",
        "SCOPE": ["email", "public_profile"],
        "AUTH_PARAMS": {"auth_type": "reauthenticate"},
        "FIELDS": ["id", "first_name", "last_name", "middle_name", "name", "name_format", "picture", "short_name"],
        "EXCHANGE_TOKEN": True,
        "VERIFIED_EMAIL": True,
        "VERSION": "v16.0",
        "GRAPH_API_URL": "https://graph.facebook.com/v16.0",
    },
}

GOOGLE_OAUTH_CALLBACK_URL = env.str("GOOGLE_OAUTH_CALLBACK_URL")

FACEBOOK_OAUTH_CALLBACK_URL = env.str("FACEBOOK_OAUTH_CALLBACK_URL")

# REST FRAMEWORK SETTINGS
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("dj_rest_auth.jwt_auth.JWTCookieAuthentication",),
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
}

# DJANGO REST SIMPLE JWT SETTINGS
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}

# DJ REST AUTH SETTINGS
REST_AUTH = {
    "JWT_AUTH_COOKIE": "engausahub-token",
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": True,
    "JWT_AUTH_SAMESITE": None,
    "PASSWORD_RESET_USE_SITES_DOMAIN": True,
    "JWT_AUTH_COOKIE_USE_CSRF": False,
    "JWT_AUTH_SECURE": DEBUG,
    "JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED": False,
    # serializers
    "LOGIN_SERIALIZER": "accounts.serializers.CustomLoginSerializer",
    "REGISTER_SERIALIZER": "accounts.serializers.CustomRegisterSerializer",
}


# CORSHEADERS SETTINGS
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")

CORS_ALLOW_CREDENTIALS = env.bool("CORS_ALLOW_CREDENTIALS")

CSRF_TRUSTED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")


# PHONE NUMBER SETTINGS
PHONENUMBER_DB_FORMAT = "INTERNATIONAL"
PHONENUMBER_DEFAULT_REGION = "NG"

# CLOUDINARY SETTINGS
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": env.str("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": env.str("CLOUDINARY_API_KEY"),
    "API_SECRET": env.str("CLOUDINARY_API_SECRET"),
}

PAYSTACK_SECRET_KEY = env.str("PAYSTACK_SECRET_KEY")


import uuid


def get_filename(filename):
    name, ext = filename.split(".")

    return f"{name}-{uuid.uuid4()[5]}.{ext}"


# ckeditor settings
CKEDITOR_UPLOAD_PATH = "uploads/ckeditor/"

CKEDITOR_FILENAME_GENERATOR = "get_filename"

CKEDITOR_ALLOW_NONIMAGE_FILES = False

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": [
            ["Bold", "Italic", "Underline", "Strike", "Subscript", "Superscript", "CodeSnippet"],
            ["NumberedList", "BulletedList", "Outdent", "Indent"],
            ["JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock"],
            ["Link", "Unlink", "Anchor"],
        ],
    }
}
