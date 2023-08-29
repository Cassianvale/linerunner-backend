# -*-coding:utf-8 -*-


from django.contrib import admin
from django.urls import path,include,re_path
from . import views
urlpatterns = [
    #发送验证码
    re_path('^smsCode/(?P<mobile>1[3-9]\d{9})$', views.SmsCodeAPIView.as_view()),


]