from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import TestCaseSerializer, TestCaseStepSerializer, BugtrackerSerializer
from utils.apiResponse import ApiResponse
from .models import TestCase, TestCaseStep, Bugtracker
from utils.pagination import CustomPagination
from ..user.permission import MyPermission
from ..user.authentications import CustomJSONWebTokenAuthentication
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.generics import get_object_or_404


class CaseResultViewSet(viewsets.ModelViewSet):
    """
    用例步骤
    """
    queryset = TestCaseStep.objects.all()
    serializer_class = TestCaseStepSerializer
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [MyPermission]

    def get(self, request, case_id=None):
        """
        获取用例的步骤
        """
        caseResult = TestCaseStep.objects.filter(case_id=case_id)
        ser = TestCaseStepSerializer(instance=caseResult, many=True).data
        return ApiResponse(data=ser)

    def put(self, request, case_id=None):
        """
        更新用例的结果
        """
        request_data = request.data
        case_steps = list(TestCaseStep.objects.filter(case_id=case_id))

        for id, case_result in enumerate(request_data):
            ser = TestCaseStepSerializer(data=case_result, instance=case_steps[id])
            if ser.is_valid(raise_exception=True):
                case_steps[id] = ser.save()

        TestCaseStep.objects.bulk_update(case_steps, ['step', 'expect', 'case_result', 'remarks'])

        # 如果用例有阻塞或者失败的，则返回失败
        case = get_object_or_404(TestCase, pk=case_id)
        case_result_set = set(TestCaseStep.objects.filter(case_id=case_id).values_list('case_result', flat=True))

        if 'fail' in case_result_set:
            case.result = 'fail'
        elif 'unexecuted' not in case_result_set:
            case.result = 'pass'
        elif 'pass' not in case_result_set:
            case.result = 'unexecuted'
        case.save()

        return ApiResponse(msg="更新成功")


class TestCaseViewSet(viewsets.ModelViewSet):

    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    pagination_class = CustomPagination
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [MyPermission]

    def modular_case(self, request, modular_id=None):
        """
        获取项目下的模块数据

        """
        case_list = TestCase.objects.filter(modular_id=modular_id)
        pg = CustomPagination()
        page_case = pg.paginate_queryset(queryset=case_list, request=request, view=self)
        ser = TestCaseSerializer(instance=page_case, many=True).data
        return pg.get_paginated_response(ser)


class BugtrackerViewSet(viewsets.ModelViewSet):

    queryset = Bugtracker.objects.all()
    serializer_class = BugtrackerSerializer
    pagination_class = CustomPagination
    permission_classes = [MyPermission]
    authentication_classes = [CustomJSONWebTokenAuthentication]

    def create(self, request, *args, **kwargs):
        """
        创建缺陷单

        """
        bugtracker = self.populate_bugtracker_from_request(Bugtracker(), request)
        bugtracker.save()
        serializer = self.get_serializer(bugtracker)
        return ApiResponse(results=serializer.data)

    def update(self, request, *args, **kwargs):
        """
        更新缺陷单

        """
        bugtracker = self.get_object()
        bugtracker = self.populate_bugtracker_from_request(bugtracker, request)
        bugtracker.save()
        # 如果处理人不为空，发送通知
        if bugtracker.handler:
            channel_layer = get_channel_layer()
            # 发送通知
            async_to_sync(channel_layer.group_send)('notifications', {
                'type': 'notification.message',
                'message': f'Bug #{bugtracker} was assigned to {bugtracker.handler}'
            })
        serializer = self.get_serializer(bugtracker)
        return ApiResponse(results=serializer.data)

    def delete(self, request, *args, **kwargs):
        """
        删除缺陷记录

        """
        bugtracker = self.get_object()
        serializer = self.get_serializer(bugtracker)
        bugtracker.delete()
        return ApiResponse(msg="删除成功！",data=serializer.data)

    def populate_bugtracker_from_request(self, bugtracker, request):
        # 获取表单数据并填充对象属性
        bugtracker.title = request.data.get('title')
        bugtracker.description = request.data.get('description')
        bugtracker.attachment = request.data.get('attachment')
        bugtracker.type = request.data.get('type')
        bugtracker.severity = request.data.get('severity')
        bugtracker.module = request.data.get('module')
        bugtracker.handler = request.data.get('handler')
        bugtracker.state = request.data.get('state')
        return bugtracker
