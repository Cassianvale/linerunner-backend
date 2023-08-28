# -*-coding:utf-8 -*-

from django.urls import path,include,re_path
from . import views
from rest_framework.routers import DefaultRouter


#实例化路由控制对象
rouer = DefaultRouter()
#项目
rouer.register('project',views.ProjectViewsets,basename='project')
#host
rouer.register('host',views.HostViewSets,basename='host')
#api
rouer.register('api',views.ApiViewsets,basename='api')
#参数化表达式
rouer.register('parameter',views.ParameterizationViewSet,basename='parameter')



urlpatterns = [
    #数据统计
    re_path('^data/$',views.DataCountView.as_view()),
    #项目---筛选查询
    path('project',views.ProjectViewsets.as_view({"get":"query_name"})),
    # host---筛选查询
    path('host', views.HostViewSets.as_view({"get": "query_name"})),
    # api---筛选查询
    path('api', views.ApiViewsets.as_view({"get": "query_name"})),
    #运行api
    path('run/api/<int:api_id>/',views.RunApiRecordAPIView.as_view()),
    # 导出api
    path('export/api/', views.ApiDumpView.as_view()),
              ]+rouer.urls