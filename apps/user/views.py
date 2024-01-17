import jwt
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from utils.apiResponse import ApiResponse
from ..user.models import User, Role, UserRole
from ..user.serializers import CustomTokenObtainPairSerializer
from ..user.serializers import UserPagingSerializer, UserCreateSerializer, UserRoleSerializer, RolePagingSerializer
from ..user.utils import jwt_response_payload_handler


class CustomTokenObtainPairView(TokenObtainPairView):
    # 刷新令牌和访问令牌
    def get_tokens_for_user(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token[0]),
        }


class UserLogin(TokenObtainPairView):
    # 使用编写的自定义序列化类
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        try:
            # 数据库加密后的密码
            db_password_hash = User.objects.get(username=username).password
        except User.DoesNotExist:
            return ApiResponse(results="ErrUserNotFound", status=status.HTTP_404_NOT_FOUND)
        # 验证明文密码跟加密后的密码是否匹配
        if not check_password(password, db_password_hash):
            return ApiResponse(results="ErrInvalidPassword", status=status.HTTP_404_NOT_FOUND)

        # 序列化处理登陆验证及数据响应
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise ValueError(f'验证失败： {e}')
        user = serializer.user
        token = serializer.validated_data["access"]
        response_data = jwt_response_payload_handler(token, user)
        return ApiResponse(msg="登录成功", data=response_data, status=status.HTTP_200_OK)


# 通用视图类
class UserViewSet(GenericViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserPagingSerializer
    permission_classes = [IsAdminUser]  # 管理员权限

    # 用户列表
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        keyword = request.GET.get("keyword")  # 查询关键字
        if keyword:
            # 用户名或昵称模糊匹配 类名.object.filter(Q(列名=值)操作符Q(列名=值))
            queryset = User.objects.filter(Q(username__icontains=keyword) | Q(nickname__icontains=keyword))

        # filter_queryset、paginate_queryset重写
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # 重写 CreateAPIView
    def create(self, request, *args, **kwargs):
        # 新建用户
        password = request.data.get("password")
        user = {
            "nickname": request.data.get("nickname"),
            "username": request.data.get("username"),
            # make_password默认pbkdf2_sha256加密
            "password": make_password(password) if password else make_password("123456")
        }
        role_names = request.data.get("roleNames")
        if "管理员" in role_names:
            user["is_staff"] = True
        else:
            user["is_staff"] = False
        user_create_serializer = UserCreateSerializer(data=user)
        user_create_serializer.is_valid(raise_exception=True)
        user_create_serializer.save()
        user_id = User.objects.get(username=user["username"]).id

        user_role = {
            "user_id": user_id,
            "role_id": ""
        }
        for role_name in role_names:
            role_id = Role.objects.get(name=role_name).id
            user_role["role_id"] = role_id
            user_role_serializer = UserRoleSerializer(data=user_role)
            user_role_serializer.is_valid(raise_exception=True)
            user_role_serializer.save()

        response_data = user_create_serializer.data
        response_data["id"] = user_id

        # 重新构建响应数据，将 user_id 放响应体最上面
        return ApiResponse(msg="创建用户成功", data={"id": user_id, **response_data},
                           status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        # 修改用户
        user = {
            "id": kwargs["pk"],  # 路径中的参数
            "username": request.data.get("username"),
            "nickname": request.data.get("nickname"),
        }
        role_names = request.data.get("roleNames")

        if role_names is not None and isinstance(role_names, (list, tuple)):
            if "管理员" in role_names:
                user["is_staff"] = True
            else:
                user["is_staff"] = False
        else:
            # 处理role_names为空或不可迭代的情况
            user["is_staff"] = False

        # 获取已有实例进行更新
        instance = self.get_object()
        user_serializer = self.get_serializer(instance, data=user)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        user_id = User.objects.get(username=user["username"]).id

        user_role = {
            "user_id": user_id,
            "role_id": ""
        }
        db_role_ids = [obj.role_id for obj in UserRole.objects.filter(user_id=user_id)]
        db_role_names = [Role.objects.get(id=db_role_id).name for db_role_id in db_role_ids]

        # 比较新旧角色差异
        new_roles = list(set(role_names).difference(db_role_names))
        old_roles = list(set(db_role_names).difference(role_names))
        for new_role in new_roles:  # 添加新角色
            role_id = Role.objects.get(name=new_role).id
            user_role["role_id"] = role_id
            user_role_serializer = UserRoleSerializer(data=user_role)
            user_role_serializer.is_valid(raise_exception=True)
            user_role_serializer.save()
        for old_role in old_roles:  # 删除老角色
            role_id = Role.objects.get(name=old_role).id
            user_role = UserRole.objects.get(user_id=user_id, role_id=role_id)
            user_role.delete()

        return ApiResponse(data=user_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        # 删除用户
        try:
            user_id = kwargs["pk"]
            user = User.objects.get(id=user_id)
            username = user.username
            user.delete()
            user_roles = UserRole.objects.filter(user_id=user_id)
            for user_role in user_roles:
                user_role.delete()
            return ApiResponse(msg="该用户数据已被删除", data={"user_id": user_id, "username": username},
                               status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return ApiResponse(results="ErrUserNotFound", status=status.HTTP_404_NOT_FOUND)

    def user_detail(self, request, *args, **kwargs):
        # 获取用户信息
        try:
            user_id = kwargs["pk"]
            user = User.objects.get(id=user_id)
            user_serializer = self.get_serializer(user)
            return Response(user_serializer.data)
        except ObjectDoesNotExist:
            return ApiResponse(results="ErrUserNotFound", status=status.HTTP_404_NOT_FOUND)


class UserInfoView(GenericViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserPagingSerializer
    permission_classes = [IsAuthenticated]  # 仅允许通过身份验证的用户

    # 获取当前登录用户信息
    def get_current_user(self, request, *args, **kwargs):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        user_serializer = self.get_serializer(user)
        return ApiResponse(msg="用户信息获取成功", data=user_serializer.data, status=status.HTTP_200_OK)


class RoleList(ListAPIView):
    # 角色列表（非常标准的REST Framework写法）
    queryset = Role.objects.all().order_by("id")
    # 序列化器
    serializer_class = RolePagingSerializer
    permission_classes = [IsAdminUser]


# 重置密码
class SystemResetPassword(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, *args, **kwargs):
        user_id = kwargs["pk"]
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return ApiResponse(results="ErrInvalidUserID", status=status.HTTP_400_BAD_REQUEST)
        user.set_password("123456")
        user.save()
        return ApiResponse(msg="密码重置成功", data={"NewPassword": "123456"}, status=status.HTTP_200_OK)


class SystemUpdatePassword(APIView):

    def put(self, request, *args, **kwargs):
        # 更新密码
        request_jwt = request.headers.get("Authorization").replace("Bearer ", "")
        request_jwt_decoded = jwt.decode(request_jwt, verify=False, algorithms=['HS256'])
        user_id = request_jwt_decoded["user_id"]  # 从jwt中解析用户id
        user = User.objects.get(id=user_id)
        db_password_hash = user.password
        old_password = request.data.get("oldPassword")
        new_password = request.data.get("newPassword")
        if not check_password(old_password, db_password_hash):  # 旧密码不匹配
            return ApiResponse(results="ErrInvalidOldPassword", status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)  # 旧密码匹配 更新密码
        user.save()
        return ApiResponse(msg="密码更新成功", data={"newpassword": new_password}, status=status.HTTP_200_OK)
