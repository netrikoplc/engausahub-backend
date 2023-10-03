from django.shortcuts import render
from allauth.socialaccount.providers.oauth2.client import OAuth2Client, OAuth2Error
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.providers.google import views as google_views
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.app_settings import api_settings
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework import status
import jwt


class GoogleOAuth2Adapter(OAuth2Adapter):
    provider_id = GoogleProvider.id
    access_token_url = google_views.ACCESS_TOKEN_URL
    authorize_url = google_views.AUTHORIZE_URL
    id_token_issuer = google_views.ID_TOKEN_ISSUER

    def complete_login(self, request, app, token, response, **kwargs):
        try:
            identity_data = jwt.decode(
                response,
                options={
                    "verify_signature": False,
                    "verify_iss": True,
                    "verify_aud": True,
                    "verify_exp": True,
                },
                issuer=self.id_token_issuer,
                audience=app.client_id,
            )
        except jwt.PyJWTError as e:
            raise OAuth2Error("Invalid id_token") from e
        login = self.get_provider().sociallogin_from_response(request, identity_data)
        return login


class GoogleLogin(SocialLoginView):
    # https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=<CALLBACK_URL>&prompt=consent&response_type=code&client_id=<CLIENT_ID>&scope=openid%20email%20profile&access_type=offline
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client


class FacebookLogin(SocialLoginView):
    # https://www.facebook.com/v16.0/dialog/oauth?client_id=<FACEBOOK_CLIENT_ID>&redirect_uri=<FACEBOOK_REDIRECT_URI>&response_type=code&display=popup
    adapter_class = FacebookOAuth2Adapter
    callback_url = settings.FACEBOOK_OAUTH_CALLBACK_URL
    client_class = OAuth2Client


class CustomLoginView(LoginView):
    def get_response(self):
        serializer_class = self.get_response_serializer()

        if api_settings.USE_JWT:
            from rest_framework_simplejwt.settings import (
                api_settings as jwt_settings,
            )

            access_token_expiration = timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME  # type: ignore
            refresh_token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME  # type: ignore
            return_expiration_times = api_settings.JWT_AUTH_RETURN_EXPIRATION
            auth_httponly = api_settings.JWT_AUTH_HTTPONLY

            data = {
                "user": self.user,
                "access": self.access_token,
            }

            if not auth_httponly:
                data["refresh"] = self.refresh_token
            else:
                # Wasnt sure if the serializer needed this
                data["refresh"] = ""

            if return_expiration_times:
                data["access_expiration"] = access_token_expiration
                data["refresh_expiration"] = refresh_token_expiration

            serializer = serializer_class(instance=data, context=self.get_serializer_context())  # type: ignore
        elif self.token:
            serializer = serializer_class(instance=self.token, context=self.get_serializer_context())  # type: ignore
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

        response = Response(serializer.data, status=status.HTTP_200_OK)
        if api_settings.USE_JWT:
            from .jwt_auth import set_jwt_cookies

            set_jwt_cookies(response, self.access_token, self.refresh_token)
        return response


class CustomLogoutView(LogoutView):
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        if api_settings.SESSION_LOGIN:
            django_logout(request)

        response = Response(
            {"detail": _("Successfully logged out.")},
            status=status.HTTP_200_OK,
        )

        if api_settings.USE_JWT:
            # NOTE: this import occurs here rather than at the top level
            # because JWT support is optional, and if `USE_JWT` isn't
            # True we shouldn't need the dependency
            from rest_framework_simplejwt.exceptions import TokenError
            from rest_framework_simplejwt.tokens import RefreshToken

            from .jwt_auth import unset_jwt_cookies

            cookie_name = api_settings.JWT_AUTH_COOKIE

            unset_jwt_cookies(response)

            if "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS:
                # add refresh token to blacklist
                try:
                    token = RefreshToken(request.data["refresh"])
                    token.blacklist()
                except KeyError:
                    response.data = {"detail": _("Refresh token was not included in request data.")}
                    response.status_code = status.HTTP_401_UNAUTHORIZED
                except (TokenError, AttributeError, TypeError) as error:
                    if hasattr(error, "args"):
                        if "Token is blacklisted" in error.args or "Token is invalid or expired" in error.args:
                            response.data = {"detail": _(error.args[0])}
                            response.status_code = status.HTTP_401_UNAUTHORIZED
                        else:
                            response.data = {"detail": _("An error has occurred.")}
                            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

                    else:
                        response.data = {"detail": _("An error has occurred.")}
                        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            elif not cookie_name:
                message = _(
                    "Neither cookies or blacklist are enabled, so the token "
                    "has not been deleted server side. Please make sure the token is deleted client side.",
                )
                response.data = {"detail": message}
                response.status_code = status.HTTP_200_OK
        return response
