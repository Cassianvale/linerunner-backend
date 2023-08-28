# -*-coding:utf-8 -*-


from django.urls import path,include,re_path
from . import views
from rest_framework.routers import DefaultRouter

rouer = DefaultRouter()
#项目
rouer.register('email',views.EmailViewSet)

urlpatterns = [
    #报告列表
    path('list/', views.ReportVIew.as_view()),
    path('list/<id>/', views.ReportVIew.as_view()),
    path('send/meail/<name>',views.mailReport),
    #报告详情
    path('<name>',views.reportDetails),

    ]+rouer.urls