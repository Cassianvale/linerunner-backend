from django.contrib import admin
from .models import *


@admin.register(Case)
class ProjectAdmin(admin.ModelAdmin):
    """自动化测试用例"""
    list_display = ['name', 'description']


@admin.register(CaseApiList)
class ProjectAdmin(admin.ModelAdmin):
    """case中的api_list"""
    list_display = ['api', 'case', 'index', 'reset_data', 'reset_expect_content', 'reset_expect_code']


@admin.register(CaseRunRecord)
class ProjectAdmin(admin.ModelAdmin):
    """用例运行记录"""
    list_display = ['case', 'create_time']


@admin.register(CaseApiRunRecord)
class ProjectAdmin(admin.ModelAdmin):
    """Case API运行记录"""
    list_display = ['name', 'url', 'http_method', 'create_time']
