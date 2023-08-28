from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class CustomJSONWebTokenAuthentication(JWTAuthentication):
    def authenticate(self, request):

        header = self.get_header(request)
        if header is None:
            raise exceptions.AuthenticationFailed('缺失JWT请求头')

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            raise exceptions.AuthenticationFailed('Authorization 字段是必须的')

        try:
            validated_token = self.get_validated_token(raw_token)
        except InvalidToken:
            raise exceptions.AuthenticationFailed('非法用户')

        user = self.get_user(validated_token)
        return user, validated_token


    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token