# -*-coding:utf-8 -*-


from rest_framework import serializers
from .models import ChanDaoModular,ChanDaoCase,ChanDaoProject,ChanDaoCaseStep
class ChanDaoProjectSerializer(serializers.ModelSerializer):
    """
    阐道-项目名称
    """
    modular_count = serializers.IntegerField(read_only=True,label="模块的用例数量")
    class Meta:
        model = ChanDaoProject
        fields = "__all__"

class ChanDaoModularSerializer(serializers.ModelSerializer):
    """
    阐道-项目模块
    """
    case_count = serializers.IntegerField(read_only=True,label="总用例")
    case_unexecuted_count = serializers.IntegerField(read_only=True,label="未执行用例")
    case_pass_count = serializers.IntegerField(read_only=True, label="通过用例")
    case_fail_count = serializers.IntegerField(read_only=True, label="失败用例")
    case_block_count = serializers.IntegerField(read_only=True, label="阻塞用例")
    class Meta:
        model = ChanDaoModular
        fields = "__all__"

class ChanDaoCaseStepSerializer(serializers.ModelSerializer):
    """
    阐道-用例步骤
    """
    class Meta:
        model = ChanDaoCaseStep
        fields = "__all__"

class ChanDaoCaseSerializer(serializers.ModelSerializer):
    """
    阐道-用例
    """
    case = ChanDaoCaseStepSerializer(many=True)
    class Meta:
        model = ChanDaoCase
        fields = "__all__"

    def create(self, validated_data):
        case_setp_list = validated_data.pop("case")
        case = ChanDaoCase.objects.create(**validated_data)
        for case_setp in case_setp_list:
            ChanDaoCaseStep.objects.create(case=case,**case_setp)
        return case

    def update(self, instance, validated_data):
        case_step_list = validated_data.pop("case")
        instance.preconditions = validated_data.get('preconditions', instance.preconditions)
        instance.case_type = validated_data.get('case_type', instance.case_type)
        instance.case_stage = validated_data.get('case_stage', instance.case_stage)
        instance.case_priority = validated_data.get('case_priority', instance.case_priority)
        instance.remarks = validated_data.get('remarks', instance.remarks)
        instance.result = validated_data.get('result', instance.result)
        instance.modular = validated_data.get('modular', instance.modular)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        ChanDaoCaseStep.objects.filter(case=instance).delete()
        for case_step in case_step_list:
            ChanDaoCaseStep.objects.create(case=instance, **case_step)
        return instance




