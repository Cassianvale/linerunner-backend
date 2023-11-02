# -*-coding:utf-8 -*-


from django.urls import path,include,re_path
from . import views
from rest_framework.routers import DefaultRouter

rouer = DefaultRouter()
#禅道---项目
rouer.register('project',views.ChanDaoProjectViewSet,basename='ChanDaoProject')
rouer.register('modular',views.ChanDaoModularViewSet,basename='ChanDaoModular')
rouer.register('case',views.ChanDaoCaseViewSet,basename='ChanDaoCase')

urlpatterns = [
            #导出测试用例
            path('export/case/<pk>/', views.CaseDumpView.as_view()),
            path('export/case/', views.CaseDumpView.as_view()),
            #下载测试用例模版
            path('excel/down/', views.ExcelDownload.as_view()),
            #导入测试用例
            path('import/case/',views.CaseImport.as_view()),

            #某个项目下的模块列表
            path('project_modular/<project_id>/',
               views.ChanDaoModularViewSet.as_view({"get": "project_modular"})),

            #某个模块下的用例列表
            path('modular_case/<modular_id>/',
               views.ChanDaoCaseViewSet.as_view({"get": "modular_case"})),

            #运行用例
            path('case/result/<case_id>/',views.CaseResult.as_view()),
            #数据统计
            path('data/count/',views.DataCountView.as_view()),

              ]+rouer.urls

