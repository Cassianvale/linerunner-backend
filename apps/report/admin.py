from django.contrib import admin
from .models import *

@admin.register(ReportModel)
class ProjectAdmin(admin.ModelAdmin):
    """接口测试报告"""
    list_display = ['project_name','project_host','case_type','case_all','case_pass','case_fail','start_time']

