from rest_framework import viewsets
from rest_framework.response import Response
from .models import Bugtracker
from .serializers import BugtrackerSerializer
from utils.apiResponse import ApiResponse
from .models import Bugtracker
from utils.pagination import CustomPagination
from ..user.permission import MyPermission
from ..user.authentications import CustomJSONWebTokenAuthentication
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


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
