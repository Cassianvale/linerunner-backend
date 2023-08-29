from django.contrib import admin

from .models import *


@admin.register(ChanDaoProject)
class ProjectAdmin(admin.ModelAdmin):
    """阐道-项目名称"""
    list_display = ['project','product_person','test_person']

@admin.register(ChanDaoModular)
class ProjectAdmin(admin.ModelAdmin):
    """阐道-模块"""
    list_display = ['project','modular']

@admin.register(ChanDaoCase)
class ProjectAdmin(admin.ModelAdmin):
    """阐道-用例"""
    list_display = ['modular','title','case_type','case_stage','result','found_time']

@admin.register(ChanDaoCaseStep)
class ProjectAdmin(admin.ModelAdmin):
    """测试步骤"""
    list_display = ['case','step','expect','case_result','remarks']

