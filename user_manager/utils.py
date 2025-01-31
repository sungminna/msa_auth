from rest_framework import status
from rest_framework.response import Response
from .serializer import KakaoUserSerializer, UserSerializer
from .models import User
from token_manager.serializer import CustomTokenObtainPairSerializer
import random

class OAuthUserManager:
    def __init__(self):
        pass

    def create_kakao_user(self, sub, nickname, email=None):
        try:
            if not email:
                email = f"{sub}@kakao.com"
            user = User.objects.filter(email=email)
            has_user = user.count() > 0
            if has_user:
                refresh = CustomTokenObtainPairSerializer.get_token(user.first())
                return refresh, user.first()
            else:
                ## give random unusable password
                password = email + str(random.random())[3:]
                serializer = UserSerializer(data={'email': email, 'nickname': nickname, 'password': password})
                if serializer.is_valid():
                    user = serializer.save()
                    user.is_active = True
                    user.save()
                    refresh = CustomTokenObtainPairSerializer.get_token(user)
                    return refresh, user
            return None, None
        except Exception as e:
            return None, None