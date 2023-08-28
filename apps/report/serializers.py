# -*-coding:utf-8 -*-

import re
from rest_framework.serializers import ModelSerializer
from .models import ReportModel,EmailModel


class ReportModelSerializer(ModelSerializer):
    class Meta:
        model = ReportModel
        fields = ['id','project_name','project_host','case_type','case_all','case_pass','case_fail','report_details','create_time']

class EmailSerializer(ModelSerializer):
    class Meta:
        model = EmailModel
        fields = "__all__"
