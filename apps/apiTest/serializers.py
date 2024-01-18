# -*-coding:utf-8 -*-

from .models import *
from rest_framework import serializers
# from apps.user.serializers import UserLoginSerializer
# from rest_framework.serializers import ValidationError
from django.db import transaction
from rest_framework import validators


class ApiArgumentSerializer(serializers.ModelSerializer):
    """
    api的全局参数
    """

    class Meta:
        model = ApiArgument
        # fields = "__all__"
        fields = ['name', 'value']


class ApiArgumentExtractSerializer(serializers.ModelSerializer):
    """
    用例API的响应参数提取
    """

    class Meta:
        model = ApiArgumentExtract
        fields = ['name', 'origin', 'format']


class ApiSerializer(serializers.ModelSerializer):
    """
    API
    """
    project_id = serializers.IntegerField(write_only=True)
    host_id = serializers.IntegerField(write_only=True)
    arguments = ApiArgumentSerializer(many=True)
    argumentExtract = ApiArgumentExtractSerializer(many=True)
    project_name = serializers.SerializerMethodField()

    class Meta:
        model = Api
        fields = "__all__"
        extra_kwargs = {
            'name': {
                'required': True,  # 设置name字段必填
                'min_length': 2,
                'error_messages': {
                    'required': '必填项',
                    'min_length': '太短',
                }
            }
        }

    def get_project_name(self, obj):
        return obj.project.name

    def create(self, validated_data):
        arguments_list = validated_data.pop('arguments')
        argumentExtract_list = validated_data.pop('argumentExtract')
        api = Api.objects.create(**validated_data)
        # 保存api的全局参数
        for arguments in arguments_list:
            ApiArgument.objects.create(api=api, **arguments)
        # 保存用例API的响应参数提取
        for argumentExtract in argumentExtract_list:
            ApiArgumentExtract.objects.create(api=api, **argumentExtract)
        return api

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                # 更新api
                arguments_list = validated_data.pop('arguments')
                argumentExtract_list = validated_data.pop('argumentExtract')
                instance.name = validated_data.get('name', instance.name)
                instance.http_method = validated_data.get('http_method', instance.http_method)
                instance.host_id = validated_data.get('host_id', instance.host_id)
                instance.path = validated_data.get('path', instance.path)
                instance.request_type = validated_data.get('request_type', instance.request_type)
                instance.data = validated_data.get('data', instance.data)
                instance.description = validated_data.get('description', instance.description)
                instance.expect_code = validated_data.get('expect_code', instance.expect_code)
                instance.headers = validated_data.get('headers', instance.headers)
                instance.expect_content = validated_data.get('expect_content', instance.expect_content)
                instance.save()
                # 删除api的全局参数和用例API的响应参数提取再新增
                ApiArgument.objects.filter(api=instance).delete()
                for arguments in arguments_list:
                    ApiArgument.objects.create(api=instance, **arguments)
                ApiArgumentExtract.objects.filter(api=instance).delete()
                for argumentExtract in argumentExtract_list:
                    ApiArgumentExtract.objects.create(api=instance, **argumentExtract)
                return instance
        except Exception as e:
            return e

    # 局部钩子
    # def validate_name(self, value):
    #     if Api.objects.filter(name=value):
    #         raise ValidationError({'name': '该名称已存在'})
    #     return value


class RunApiRecordSerializer(serializers.ModelSerializer):
    """
    API运行记录
    """
    project_name = serializers.SerializerMethodField()

    class Meta:
        model = RunApiRecord
        fields = "__all__"

    def get_project_name(self, obj):
        return obj.api.project.name


class ParameterizationSerializer(serializers.ModelSerializer):
    """
    参数化表达式
    """

    class Meta:
        model = Parameterization
        fields = "__all__"
