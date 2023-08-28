# -*-coding:utf-8 -*-

from .models import Case,CaseApiList,CaseRunRecord,CaseApiRunRecord
from ..apiTest.serializers import ApiSerializer
from rest_framework import serializers

class CaseApiListSerializer(serializers.ModelSerializer):
    """
    case中的api_list
    """
    class Meta:
        model = CaseApiList
        # fields = "__all__"
        exclude = ('id',)

class CaseSerializer(serializers.ModelSerializer):
    """
    自动化测试用例
    """
    api_list = CaseApiListSerializer(many=True)

    class Meta:
        model = Case
        fields = "__all__"
        # fields = ['id','name','api_list']

    def create(self, validated_data):
        api_list = validated_data.pop('api_list')
        case = Case.objects.create(**validated_data)
        for api in api_list:
            CaseApiList.objects.create(case=case,**api)
        return case

    def update(self,instance, validated_data):
        api_list = validated_data.pop('api_list')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        CaseApiList.objects.filter(case=instance).delete()
        for api in api_list:
            CaseApiList.objects.create(case=instance, **api)
        return instance


class CaseApiRunRecordSerializer(serializers.ModelSerializer):
    """
    case api运行记录
    """
    api = ApiSerializer()
    class Meta:
        model = CaseApiRunRecord
        fields = "__all__"

class CaseRunRecordSerializer(serializers.ModelSerializer):
    """
    用例运行记录
    """
    api_records = CaseApiRunRecordSerializer(many=True)
    case = CaseSerializer()
    class Meta:
        model = CaseRunRecord
        fields = "__all__"
