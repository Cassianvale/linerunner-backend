# -*-coding:utf-8 -*-


import json
from rest_framework import serializers
from .models import TestTask,CrontabTask
from ..case.serializers import CaseSerializer
from rest_framework.serializers import ValidationError

class TestTaskModelSerializer(serializers.ModelSerializer):
    """
    测试任务
    """
    class Meta:
        model = TestTask
        fields = "__all__"

class CrontabTaskSerializer(serializers.ModelSerializer):
    # 验证，序列化
    # project_id = serializers.IntegerField(write_only=True)
    # case_id = serializers.CharField(write_only=True)
    expr = serializers.CharField(max_length=100)
    status = serializers.IntegerField(read_only=True)
    case = CaseSerializer(read_only=True)
    class Meta:
        model = CrontabTask
        fields = ['id','name','expr','status','case_id','case']

    def validate_expr(self,value):
        """
        表达式验证
        :param value:
        :return:
        """
        res = json.loads(value)
        if type(res)!=dict:
            raise ValidationError({"expr":"字段格式错误"})
        return value

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        if instance.status==1:
            raise ValidationError({"status": "任务进行中，不能进行编辑"})
        elif instance.status==2:
            # CrontabTask.objects.create(pk=instance,**validated_data)
            instance.name = validated_data.get('name', instance.name)
            instance.expr = validated_data.get('expr', instance.expr)
            instance.case_id = validated_data.get('case_id', instance.case_id)
            instance.name = validated_data.get('name', instance.name)
            instance.save()
            return instance





