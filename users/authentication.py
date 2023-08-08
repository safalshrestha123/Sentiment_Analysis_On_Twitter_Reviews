import datetime
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from datetime import date, timedelta
from django.utils import timezone
from django.conf import settings
import datetime
import pytz

# #this return left time
# def expires_in(token):
#     time_elapsed = timezone.now() - token.created
#     left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
#     return left_time

# # token checker if token expired or not
# def is_token_expired(token):
#     return expires_in(token) < timedelta(seconds = 0)

# # if token is expired new token will be established
# # If token is expired then it will be removed
# # and new one with different key will be created
# def token_expire_handler(token):
#     is_expired = is_token_expired(token)
#     if is_expired:
#         token.delete()
#         token = Token.objects.create(user = token.user)
#     return is_expired, token

#DEFAULT_AUTHENTICATION_CLASSES
class ExpiringTokenAuthentication(TokenAuthentication):
    """
    If token is expired then it will be removed
    and new one with different key will be created
    """
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key = key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid Token!!")
        
        if not token.user.is_active:
            raise AuthenticationFailed("User is not active")

        utc_now = datetime.datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - datetime.timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS):
            raise  AuthenticationFailed("Token has expired...")
        
        return (token.user, token)