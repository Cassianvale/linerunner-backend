# -*-coding:utf-8 -*-

from .models import Case
from ..apiTest.models import RunApiRecord
from ..apiTest.serializers import RunApiRecordSerializer
from .serializers import CaseSerializer, CaseRunRecordSerializer
from utils.apiResponse import ApiResponse
from utils.pagination import CustomPagination
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from linerunner.settings import logger
from .run_case import run_case,run_case_list
from .models import CaseRunRecord
from ..user.authentications import CustomJSONWebTokenAuthentication
from ..user.permission import MyPermission

class CaseViewsets(ModelViewSet):
    """
    测试用例
    """
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    pagination_class = CustomPagination
    permission_classes = [MyPermission]
    authentication_classes = [CustomJSONWebTokenAuthentication]

    #筛选
    @action(methods=['get'],detail=False)
    def query_name(self, request, *args,**kwargs):
        case_name = Case.objects.filter(name__contains=self.request.query_params.get('name',''))
        ser = CaseSerializer(case_name,many=True)
        return ApiResponse(results=ser.data)

class CaseRunApiView(APIView):
    permission_classes = [MyPermission]
    authentication_classes = [CustomJSONWebTokenAuthentication]

    """
    单条测试用例运行
    """
    def post(self,request,case_id):
        logger.info("执行测试用例id:{}".format(case_id))
        run_case(case_id)
        return ApiResponse(results="测试用例运行成功")

class CaseListApiRunRecordAPIView(APIView):
    permission_classes = [MyPermission]
    authentication_classes = [CustomJSONWebTokenAuthentication]

    """
    批量运行测试用例
    """
    def post(self, request, *args, **kwargs):
        case_id_list = request.data.get("case_id_list")
        run_case_list(case_id_list)
        return ApiResponse(results="批量测试用例运行成功")

class RecordView(APIView):
    """
    case运行记录
    """
    pagination_class = CustomPagination
    permission_classes = [MyPermission]
    authentication_classes = [CustomJSONWebTokenAuthentication]

    def get(self,request):
        #通过type区分是api运行记录还是case运行记录
        #通过id查询具体用例
        type = request.GET.get('type')
        project_id = request.GET.get('project')
        logger.info("record_type:{}".format(type))
        logger.info("project_id:{}".format(project_id))
        if type == 'api':
            #单查
            if project_id:
                records = RunApiRecord.objects.filter(id=project_id)
                pg = CustomPagination()
                page_records = pg.paginate_queryset(queryset=records,request=request,view=self)
                serializer = RunApiRecordSerializer(instance=page_records,many=True)
                return ApiResponse(results=serializer.data)
            #群查
            else:
                records = RunApiRecord.objects.filter()
                pg = CustomPagination()
                page_records = pg.paginate_queryset(queryset=records,request=request,view=self)
                serializer = RunApiRecordSerializer(instance=page_records,many=True).data
                return pg.get_paginated_response(serializer)
        elif type=="case":
            #单查
            if project_id:
                records = CaseRunRecord.objects.filter(case__project_id=project_id)
                pg = CustomPagination()
                page_records = pg.paginate_queryset(queryset=records, request=request, view=self)
                serializer = CaseRunRecordSerializer(instance=page_records, many=True).data
                return pg.get_paginated_response(serializer)
            else:
                records = CaseRunRecord.objects.filter()
                pg = CustomPagination()
                page_records = pg.paginate_queryset(queryset=records, request=request, view=self)
                serializer = CaseRunRecordSerializer(instance=page_records, many=True).data
                return pg.get_paginated_response(serializer)
        else:
            return ApiResponse(results="参数错误")