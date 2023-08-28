from rest_framework import status
from rest_framework.views import exception_handler
from ..user.models import Role, UserRole
from ..user.serializers import RoleAuthSerializer
from ..user.serializers import UserLoginSerializer


def jwt_response_payload_handler(token, user=None):
    # 自定义响应体
    role_id = UserRole.objects.get(user_id=user.id).role_id  # 获取角色id
    # 登录返回token、用户信息、角色权限
    return {
        "token": token,
        "user": UserLoginSerializer(user).data,
        "auth": RoleAuthSerializer(Role.objects.get(id=role_id)).data["auth"]  # 根据角色id获取菜单
    }


def custom_exception_handler(exc, context):
    # 根据异常自定义响应体和状态码
    if hasattr(exc, "detail"):
        if exc.detail == "缺失JWT请求头":
            response = exception_handler(exc, context)
            response.data = {
                "msg": "缺失JWT请求头",
                "data": {}
            }
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return response
        if exc.detail == "签名已过期":
            response = exception_handler(exc, context)
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return response
    return exception_handler(exc, context)

