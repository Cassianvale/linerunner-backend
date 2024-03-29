from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class BaseTable(models.Model):
    # 基础日期字段 统一添加创建时间和更新时间字段
    class Meta:
        abstract = True  # 不会创建表
        db_table = 'BaseTable'

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)


# 具有符合管理员权限的功能齐全的用户模型,需要用户名密码，其他可选
class User(AbstractUser):
    class Meta:
        db_table = "user"
        verbose_name = "用户表"

    REQUIRED_FIELDS = []  # 让Django默认必填的邮箱变成非必填
    nickname = models.CharField("昵称", max_length=64, null=False, default="")


class Role(BaseTable):
    # 角色表
    class Meta:
        db_table = "role"
        verbose_name = "角色表"

    name = models.CharField("角色名", max_length=64, null=False, default="")
    # 可访问的菜单权限
    auth = models.JSONField("菜单权限JSON", default=None)


class UserRole(BaseTable):
    # 用户角色关系表
    class Meta:
        db_table = "user_role"
        verbose_name = "用户权限表"

    user_id = models.IntegerField("用户id", null=False, default=0)
    role_id = models.IntegerField("角色id", null=False, default=0)
