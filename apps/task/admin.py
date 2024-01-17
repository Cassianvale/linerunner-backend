from django.contrib import admin
from .models import *


@admin.register(TestTask)
class ProjectAdmin(admin.ModelAdmin):
    """测试任务"""
    list_display = ['month', 'task_name', 'tester', 'develop', 'start_time', 'end_time', 'publish_time']


@admin.register(CrontabTask)
class ProjectAdmin(admin.ModelAdmin):
    """定时任务"""
    list_display = ['name', 'case_id', 'expr', 'status']
