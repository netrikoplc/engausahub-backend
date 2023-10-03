from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from dj_rest_auth.app_settings import api_settings
from django.conf import settings


def set_jwt_access_cookie(response, access_token):
    from rest_framework_simplejwt.settings import api_settings as jwt_settings

    cookie_name = api_settings.JWT_AUTH_COOKIE
    access_token_expiration = timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME  # type:ignore
    cookie_secure = api_settings.JWT_AUTH_SECURE
    cookie_httponly = api_settings.JWT_AUTH_HTTPONLY
    cookie_samesite = api_settings.JWT_AUTH_SAMESITE
    cookie_domain = getattr(settings, "JWT_AUTH_COOKIE_DOMAIN")

    if cookie_name:
        response.set_cookie(
            cookie_name,
            access_token,
            expires=access_token_expiration,
            secure=cookie_secure,
            httponly=cookie_httponly,
            samesite=cookie_samesite,
            domain=cookie_domain,
        )


def set_jwt_refresh_cookie(response, refresh_token):
    from rest_framework_simplejwt.settings import api_settings as jwt_settings

    refresh_token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME  # type:ignore
    refresh_cookie_name = api_settings.JWT_AUTH_REFRESH_COOKIE
    refresh_cookie_path = api_settings.JWT_AUTH_REFRESH_COOKIE_PATH
    cookie_secure = api_settings.JWT_AUTH_SECURE
    cookie_httponly = api_settings.JWT_AUTH_HTTPONLY
    cookie_samesite = api_settings.JWT_AUTH_SAMESITE
    cookie_domain = getattr(settings, "JWT_AUTH_COOKIE_DOMAIN")

    if refresh_cookie_name:
        response.set_cookie(
            refresh_cookie_name,
            refresh_token,
            expires=refresh_token_expiration,
            secure=cookie_secure,
            httponly=cookie_httponly,
            samesite=cookie_samesite,
            path=refresh_cookie_path,
            domain=cookie_domain,
        )


def set_jwt_cookies(response, access_token, refresh_token):
    set_jwt_access_cookie(response, access_token)
    set_jwt_refresh_cookie(response, refresh_token)


def unset_jwt_cookies(response):
    cookie_name = api_settings.JWT_AUTH_COOKIE
    refresh_cookie_name = api_settings.JWT_AUTH_REFRESH_COOKIE
    refresh_cookie_path = api_settings.JWT_AUTH_REFRESH_COOKIE_PATH
    cookie_samesite = api_settings.JWT_AUTH_SAMESITE
    cookie_domain = getattr(settings, "JWT_AUTH_COOKIE_DOMAIN")

    if cookie_name:
        response.delete_cookie(cookie_name, samesite=cookie_samesite, domain=cookie_domain)
    if refresh_cookie_name:
        response.delete_cookie(
            refresh_cookie_name, path=refresh_cookie_path, samesite=cookie_samesite, domain=cookie_domain
        )
