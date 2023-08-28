# -*-coding:utf-8 -*-

from django.urls import path,include,re_path
from . import views
from rest_framework.routers import DefaultRouter

rouer = DefaultRouter()
#case
rouer.register('case',views.CaseViewsets,basename='case')


urlpatterns = [
        #运行单条测试用例
        path('run/<case_id>/',views.CaseRunApiView.as_view()),
        #运行多条测试用例
        re_path('runList/',views.CaseListApiRunRecordAPIView.as_view()),
        #查看运行记录
        path('record',views.RecordView.as_view()),
        #测试用例---查询
        path('case',views.CaseViewsets.as_view({"get":"query_name"})),
              ]+rouer.urls