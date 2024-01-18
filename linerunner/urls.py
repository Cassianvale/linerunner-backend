from django.contrib import admin
from django.urls import path, include
# yasg的视图配置类，用于生成api
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="drf接口文档",  # 必须
        default_version="v1.0.0",  # 必须
        description="描述",
        terms_of_service='',
        contact=openapi.Contact(email=""),
        license=openapi.License(name="协议版本")
    ),
    public=True,  # 所有人访问
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # user 用户
    path('users/', include('apps.user.urls')),
    # 测试跟踪
    path('test/', include('apps.test.urls')),
    # 测试管理
    path('project/', include('apps.project.urls')),
    # # apiTest
    # path('api/', include('apps.apiTest.urls')),
    # case 用例
    # path('case/', include('apps.case.urls')),
    # 禅道
    # path('chandao/', include('apps.chanDao.urls')),

    # # 报告
    # path('report/', include('apps.report.urls')),
    # # 任务
    # path('task/', include('apps.task.urls')),
    # # xmind
    # path('xm/', include('apps.xmfile.urls')),
    # swag接口文档
    path('docs/', schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger"),
]
