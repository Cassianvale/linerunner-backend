#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

rouer = DefaultRouter()
# 测试用例
rouer.register('testcase', views.TestCaseViewSet, basename='TestCase')
# 用例步骤
rouer.register('casestep', views.CaseResultViewSet, basename='CaseStep')
# bug跟踪
rouer.register('bug', views.BugtrackerViewSet, basename='Bug')

urlpatterns = [
                  # # 某个项目下的模块列表
                  # path('project_modular/<project_id>/',
                  #      views.ModularViewSet.as_view({"get": "project_modular"})),
                  #
                  # # 某个模块下的用例列表
                  # path('modular_case/<modular_id>/',
                  #      views.TestCaseViewSet.as_view({"get": "modular_case"})),

                  path('bug', views.BugtrackerViewSet.as_view({"get": "query_name"})),
                  path('bug/<int:pk>/', views.BugtrackerViewSet.as_view({"get": "retrieve"})),
                  path('bug/create', views.BugtrackerViewSet.as_view({"post": "create"})),
                  path('bug/<int:pk>/update', views.BugtrackerViewSet.as_view({"put": "update"})),
                  path('bug/<int:pk>/delete', views.BugtrackerViewSet.as_view({"delete": "destroy"})),
              ] + rouer.urls
