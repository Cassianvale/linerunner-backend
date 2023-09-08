from rest_framework import serializers
from ..user.models import User, Role, UserRole
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 从数据库种获取
        fields = ['username', 'nickname', 'roleName']

    # 定义登录的返回字段
    # 固定写法，表示是通过自定义方法取值
    roleName = serializers.SerializerMethodField()

    def get_roleName(self, instance):
        # 从instance中获取用户的id，instance就是class Meta里面指定的model
        user_id = instance.id
        # 查询UserRole模型，获取与该用户相关的角色的role_id列表
        role_ids = [obj.role_id for obj in UserRole.objects.filter(user_id=user_id)]
        # 查询Role模型，获取每个角色的名称
        query_set = [Role.objects.get(id=role_id) for role_id in role_ids]
        return ", ".join([obj.name for obj in query_set])


# 重写 TokenObtainPairSerializer 自定义令牌的生成方式
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)
    

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'nickname', 'password', "is_staff"]


class UserPagingSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    roleNames = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'roleNames', "is_staff"]

    def get_roleNames(self, instance):
        user_id = instance.id
        role_ids = [obj.role_id for obj in UserRole.objects.filter(user_id=user_id)]
        query_set = [Role.objects.get(id=role_id) for role_id in role_ids]
        return [{"id": obj.id, "name": obj.name} for obj in query_set]


class RoleAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['auth']


class RolePagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name"]


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['user_id', 'role_id']
