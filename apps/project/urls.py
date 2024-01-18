#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter

rouer = DefaultRouter()
# 项目管理
rouer.register('项目管理', views.Project, basename='Project')
# 模块管理
rouer.register('模块管理', views.Modular, basename='Modular')
# 环境变量
rouer.register('环境变量', views.Host, basename='Host')

