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
        contact=openapi.Contact(email="1430066373@qq.com"),
        license=openapi.License(name="协议版本")
    ),
    public=True,  # 所有人访问
    # permission_classes=[rest_framework.permissions.AllowAny],  # 权限类，和上面的互斥
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # user 用户
    path('users/', include('apps.user.urls')),
    # apiTest
    path('api/', include('apps.apiTest.urls')),
    # case 用例
    path('case/', include('apps.case.urls')),
    # swag接口文档
    path('docs/', schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger"),
]
