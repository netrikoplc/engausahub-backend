from django.shortcuts import render
from allauth.socialaccount.providers.oauth2.client import OAuth2Client, OAuth2Error
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.providers.google import views as google_views
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from django.conf import settings
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
