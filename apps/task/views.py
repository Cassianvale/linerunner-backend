# -*-coding:utf-8 -*-


from django.shortcuts import render
from .models import TestTask, CrontabTask
from .serializers import TestTaskModelSerializer, CrontabTaskSerializer
from rest_framework import viewsets
from utils.pagination import CustomPagination
from ..user.permission import MyPermission
from ..user.authentications import CustomJSONWebTokenAuthentication
from rest_framework.views import APIView
from linerunner.settings import logger
from utils.apiResponse import ApiResponse
from . import scheduler
from rest_framework import status
from django.db import transaction
import xlrd

from rest_framework.decorators import action


class TestTaskViewsets(viewsets.ModelViewSet):
    """
    测试任务
    """
    queryset = TestTask.objects.all()
    serializer_class = TestTaskModelSerializer
    pagination_class = CustomPagination
    permission_classes = [MyPermission]
    authentication_classes = [CustomJSONWebTokenAuthentication]

    # 筛选
    @action(methods=['get'], detail=False)
    def query_name(self, request, *args, **kwargs):
        testTask_task_name = TestTask.objects.filter(task_name__contains=self.request.query_params.get('task_name', ''))
        ser = TestTaskModelSerializer(testTask_task_name, many=True)
        return ApiResponse(results=ser.data)


class CrontabTaskViewsets(viewsets.ModelViewSet):
    """
    定时任务
    """
    queryset = CrontabTask.objects.all()
    serializer_class = CrontabTaskSerializer
    pagination_class = CustomPagination
    permission_classes = [MyPermission]
    authentication_classes = [CustomJSONWebTokenAuthentication]


class StartStopTaskView(APIView):
    """
    启用定时任务
    """
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [MyPermission]

    def post(self, request, task_id, target_status):
        task = CrontabTask.objects.get(pk=task_id)
        logger.info("task:{}".format(task))
        # 如果是想要运行任务
        if target_status == 1:
            if task.status == 1:
                # 任务正在运行，不需要重复运行
                return ApiResponse(status=1, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR, msg="错误",
                                   results="状态异常")
            scheduler.add_task(task)

            task.status = 1  # 更改当前任务的状态
        elif target_status == 2:
            if task.status == 2:
                # 任务已经停止，不需要重复停止
                return ApiResponse(status=1, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR, msg="错误",
                                   results="状态异常")
            scheduler.remove_task(task)
            task.status = 2
        else:
            return ApiResponse(status=1, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR, msg="错误",
                               results="状态异常")
        task.save()
        return ApiResponse(results=CrontabTaskSerializer(task).data)
