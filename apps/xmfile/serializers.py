# -*-coding:utf-8 -*-


import os
from rest_framework import serializers
from ..xmfile.models import XmFileModel
from utils.upload_oss import UploadOss
from django.db import transaction
class XmFileSerializer(serializers.ModelSerializer):
    """
    xmind文件
    """
    class Meta:
        model = XmFileModel
        fields = "__all__"

    def create(self, validated_data):
        """
        添加xmind文件
        """
        local_path = validated_data['path']
        # 将报告上传oss
        file_name = local_path.split("/")[1]
        BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        xmind_add = os.path.join(BASE_PATH,"../file/") + file_name
        oss_path = UploadOss().oss_file(file_name, xmind_add)
        validated_data['path'] = oss_path
        xm_file = XmFileModel.objects.create(**validated_data)
        return xm_file










