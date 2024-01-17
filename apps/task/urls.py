# -*-coding:utf-8 -*-


from django.urls import path, include, re_path
from . import views
from rest_framework.routers import DefaultRouter

rouer = DefaultRouter()
# 测试任务
rouer.register('test', views.TestTaskViewsets, basename='TestTask')
# 定时任务
rouer.register('crontab', views.CrontabTaskViewsets)

urlpatterns = [
                  # 启动/停止定时任务
                  path('startStop/<int:task_id>/<int:target_status>', views.StartStopTaskView.as_view()),
                  # 测试任务---查询
                  path('test', views.TestTaskViewsets.as_view({"get": "query_name"})),
                  # path('data',views.TestData.as_view())
              ] + rouer.urls
