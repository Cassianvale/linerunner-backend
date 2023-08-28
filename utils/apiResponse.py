# -*-coding:utf-8 -*-
from rest_framework.response import Response


class ApiResponse(Response):
    def __init__(self, code=0, msg="ok", data=None, results=None, http_status=None, headers=None, exception=None,**kwargs ):

        if results == "ErrUserNotFound":
            code = 404
            msg = "该用户不存在"
            data = {}
        elif results == "ErrInvalidPassword":
            code = 404
            msg = "用户名密码不匹配"
            data = {}
        elif results == "ErrInvalidOldPassword":
            code = 400
            msg = "初始密码错误"
            data = {}
        elif results == "ErrInvalidUserID":
            code = 400
            msg = "无效的用户ID"
            data = {}
        elif results == "ErrRoleNotFound":
            code = 404
            msg = "该角色不存在"
            data = {}

        response_data = {
            "code": code,
            "msg": msg,
            "data": data,
        }

        super().__init__(data=response_data, status=http_status, headers=headers, exception=exception)

