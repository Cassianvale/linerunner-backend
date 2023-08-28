# -*-coding:utf-8 -*-
from rest_framework import status
from utils.apiResponse import ApiResponse
from rest_framework.permissions import BasePermission
from rest_framework.renderers import JSONRenderer

class MyPermission(BasePermission):
    """
    权限
    """
    def has_permission(self, request, view):
        # 判断该用户有没有权限
        if request.method in ["POST", "PUT", "DELETE"]:
            if request.data.get("is_staff") == True:
                return True
            else:
                
                return ApiResponse(code="3", msg="无访问权限，请联系管理员", status=status.HTTP_403_FORBIDDEN)
        else:
            return True