from django.contrib import admin
from .models import *

admin.site.site_header = "LineRunner"
admin.site.site_title = "LineRunner"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """项目表"""
    list_display = ['name', 'type', 'description']


@admin.register(Host)
class ProjectAdmin(admin.ModelAdmin):
    """host"""
    list_display = ['name', 'host', 'description', 'project']


@admin.register(Api)
class ProjectAdmin(admin.ModelAdmin):
    """api接口"""
    list_display = ['name', 'http_method', 'host', 'project', 'path', 'headers', 'request_type', 'data', 'description',
                    'expect_code']


@admin.register(ApiArgument)
class ProjectAdmin(admin.ModelAdmin):
    """api的全局参数"""
    list_display = ['api', 'name', 'value']


@admin.register(ApiArgumentExtract)
class ProjectAdmin(admin.ModelAdmin):
    """用例API的响应参数提取"""
    list_display = ['api', 'name', 'origin', 'format']


@admin.register(RunApiRecord)
class ProjectAdmin(admin.ModelAdmin):
    """API运行记录"""
    list_display = ['url', 'http_method', 'create_time']
