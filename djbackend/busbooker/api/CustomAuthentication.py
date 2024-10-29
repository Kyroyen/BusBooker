from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt
from datetime import datetime, timedelta
from django.core.cache import cache

from django.conf import settings

class CustomAuthentication:
    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION').split()
        if len(auth) == 1:
            msg = ('Invalid token header. No credentials provided.')
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = ('Invalid token header. Token string should not contain spaces.')
            raise AuthenticationFailed(msg)
        token = auth[1]
        return self.check_auth_token(token)
        
    def check_auth_token(self, user_token):
        try:
            decoded = jwt.decode(
                user_token, settings.SECRET_KEY, algorithms=['HS256']
            )
            username = decoded['username']
            cache_key = f"username_user:{username}"
            user = cache.get(cache_key)
            if user is None:
                user = User.objects.get(username=username)
                cache.set(cache_key,  user, 120)
            return user
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Expired token')
        except Exception:
            raise AuthenticationFailed('Invalid token')
        
    def create_auth_token(self, user):
        token_data = {
            "username" : user.username,
            "exp": datetime.now() + timedelta(minutes=30)
        }
            
        encoded_token = jwt.encode(
            payload = token_data,
            key = settings.SECRET_KEY,
            algorithm= "HS256",
        )
        return encoded_token
        