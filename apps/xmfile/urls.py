# -*-coding:utf-8 -*-


from django.urls import path,include,re_path
from . import views
from rest_framework.routers import DefaultRouter
rouer = DefaultRouter()
#
rouer.register('xmind',views.XmFileViewSet)

urlpatterns = [
    #上传xmind文件
    path('file', views.UploadFile.as_view()),
    path('file/<pk>', views.DownFile.as_view()),
]+rouer.urls