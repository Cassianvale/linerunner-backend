#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .models import Project, Modular, Host
from rest_framework import serializers
from rest_framework import validators


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目管理
    """
    name = serializers.CharField(max_length=50, label="项目名称", help_text='项目名称',
                                 validators=[validators.UniqueValidator(queryset=Project.objects.all(),
                                                                        message="项目名称重复")])
    modular_count = serializers.IntegerField(read_only=True, label="模块的用例数量")

    class Meta:
        model = Project
        fields = ['id', 'name', 'type', 'description', 'modular_count']
        extra_kwargs = {
            "name": {
                'required': True
            }
        }


class ModularSerializer(serializers.ModelSerializer):
    """
    项目模块
    """
    case_count = serializers.IntegerField(read_only=True, label="总用例")
    case_unexecuted_count = serializers.IntegerField(read_only=True, label="未执行用例")
    case_pass_count = serializers.IntegerField(read_only=True, label="通过用例")
    case_fail_count = serializers.IntegerField(read_only=True, label="失败用例")
    case_block_count = serializers.IntegerField(read_only=True, label="阻塞用例")

    class Meta:
        model = Modular
        fields = "__all__"


class HostSerializer(serializers.ModelSerializer):
    """
    环境变量
    """
    project_id = serializers.IntegerField()

    class Meta:
        model = Host
        fields = ['id', 'name', 'description', 'project_id', 'host']
        extra_kwargs = {
            "name": {
                'required': True
            }
        }


