from rest_framework import serializers
from .models import TestCase, TestCaseStep, Bugtracker


class TestCaseStepSerializer(serializers.ModelSerializer):
    """
    用例步骤
    """

    class Meta:
        model = TestCaseStep
        fields = "__all__"


class TestCaseSerializer(serializers.ModelSerializer):
    """
    测试用例
    """
    case = TestCaseStepSerializer(many=True)

    class Meta:
        model = TestCase
        fields = "__all__"

    def create(self, validated_data):
        case_setp_list = validated_data.pop("case")
        case = TestCase.objects.create(**validated_data)
        case_steps = [TestCaseStep(case=case, **case_step) for case_step in case_setp_list]
        TestCaseStep.objects.bulk_create(case_steps)
        return case

    def update(self, instance, validated_data):
        case_step_list = validated_data.pop("case")
        instance.update(**validated_data)
        instance.save()

        # Get existing case steps
        existing_steps = {step.id: step for step in TestCaseStep.objects.filter(case=instance)}

        # Updated and new case steps
        updated_steps = []
        new_steps = []

        for case_step in case_step_list:
            if 'id' in case_step and case_step['id'] in existing_steps:
                updated_steps.append(TestCaseStep(case=instance, **case_step))
                del existing_steps[case_step['id']]
            else:
                new_steps.append(TestCaseStep(case=instance, **case_step))

        # Updated case steps
        TestCaseStep.objects.bulk_update(updated_steps, ['step', 'expect', 'case_result', 'remarks'])

        # New case steps
        TestCaseStep.objects.bulk_create(new_steps)

        # Deleted case steps
        TestCaseStep.objects.filter(id__in=existing_steps.keys()).delete()

        return instance


class BugtrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bugtracker
        fields = ('id', 'title', 'description', 'attachment', 'type', 'severity', 'module', 'handler', 'state')
