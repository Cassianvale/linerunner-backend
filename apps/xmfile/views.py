# -*-coding:utf-8 -*-

import os
from django.shortcuts import render
from utils.apiResponse import ApiResponse
from utils.upload_oss import UploadOss
from utils.modelViewSet import APIModelViewSet
from rest_framework.views import APIView
from linerunner.settings import UPLOAD_ROOT
from apps.xmfile.models import XmFileModel
from apps.xmfile.serializers import XmFileSerializer
from utils.pagination import CustomPagination
from ..user.authentications import CustomJSONWebTokenAuthentication
from ..user.permission import MyPermission
from django.http import FileResponse


class UploadFile(APIView):
    def post(self, request):
        # 获取上传文件
        file = request.FILES.get('file', None)
        if file is None:
            return ApiResponse(status=1, msg="请选择上传文件")
        else:
            if file.name.endswith(('.xmind')):
                destinstion = open(os.path.join(UPLOAD_ROOT, file.name), 'wb+')
            else:
                return ApiResponse(status=1, msg="文件格式错误，只支持.xmind文件")
            try:
                for chunk in file.chunks():
                    destinstion.write(chunk)
                destinstion.close()
            except Exception as e:
                return ApiResponse(status=1, msg="数据异常")
        return ApiResponse(results=destinstion.name)

class DownFile(APIView):
    def get(self,request,pk):
        file_name = XmFileModel.objects.get(id=pk).suffix_name
        BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        yourLocalFile = os.path.join(BASE_PATH, '../file/') + file_name
        UploadOss().oss_down(file_name, yourLocalFile)
        BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(BASE_PATH, '../file/') + file_name
        file = open(path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name).encode()
        return response

class XmFileViewSet(APIModelViewSet):

    queryset = XmFileModel.objects.all()
    serializer_class = XmFileSerializer
    pagination_class = CustomPagination
    # permission_classes = [MyPermission]
    # authentication_classes = [CustomJSONWebTokenAuthentication]