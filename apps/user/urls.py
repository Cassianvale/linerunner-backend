from django.urls import path
from ..user import views

urlpatterns = [
    # 登录 返回token /users/login
    path(r"login", views.UserLogin.as_view()),
    # 获取当前登录用户信息 /users/info
    path(r"info", views.UserInfoView.as_view({
        'get': 'get_current_user',
    })),

    path(r"", views.UserViewSet.as_view({
        "get": "list",  # 用户列表
        "post": "create",  # 新增用户

    })),
    
    path(r"<int:pk>", views.UserViewSet.as_view({
        "get": "user_detail",  # 用户信息
        "put": "put",  # 修改用户
        "delete": "delete"  # 删除用户
    })),

    # 重置密码
    path(r"<int:pk>/passwords/reset", views.SystemResetPassword.as_view()),

    # 角色列表
    path(r"roles", views.RoleList.as_view()),

    # 修改密码
    path(r"passwords/set", views.SystemUpdatePassword.as_view()),


]
