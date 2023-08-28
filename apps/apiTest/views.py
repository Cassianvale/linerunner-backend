import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
import datetime
import xlrd
import json
from rest_framework import status
from .models import Project,Api,Host,ApiArgumentExtract,ApiArgument,RunApiRecord,Parameterization
from .serializers import ProjectSerializer,HostSerializer,ApiSerializer,ApiArgumentExtractSerializer,ApiArgumentSerializer,RunApiRecordSerializer,ParameterizationSerializer
from .api_request import apiRequest
from utils.apiResponse import ApiResponse
from utils.pagination import CustomPagination
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView
from django.contrib.auth import get_user_model
from linerunner.settings import logger
from ..case.models import Case
from utils.dictor import dictor
users = get_user_model()
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BaseAuthentication
from ..user.authentications import JWTAuthentication, CustomJSONWebTokenAuthentication
from ..user.permission import MyPermission
from django.db import transaction
from ast import literal_eval
from .excel import *
from utils.modelViewSet import APIModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ApiFilter
from rest_framework.generics import GenericAPIView
class DataCountView(APIView):
    """
    项目管理数据统计
    """
    permission_classes = [MyPermission]
    authentication_classes = [CustomJSONWebTokenAuthentication]

    def get(self,request):
        #基础数据"总项目数，总域名，总接口数，总用例数"
        project_count = Project.objects.count()
        host_count = Host.objects.count()
        api_count = Api.objects.count()
        case_count = Case.objects.count()
        #总自动化用例近5天编写情况
        api_write_list = []
        case_write_list = []
        for day in range(5):
            threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days=day))
            otherStyleTime = threeDayAgo.strftime("%Y-%m-%d")
            # api近5日编写统计情况
            api_counts = Api.objects.filter(create_time__contains=otherStyleTime).count()
            api_write_list.append({"time":otherStyleTime,"api_count":api_counts})
            #case近5日编写统计情况
            case_counts = Case.objects.filter(create_time__contains=otherStyleTime).count()
            case_write_list.append({"time":otherStyleTime,"case_count":case_counts})
        count_all = {"project_count":project_count,
                     "host_count":host_count,
                     "api_count":api_count,
                     "case_count":case_count,
                     "api_write_list":api_write_list,
                     "case_write_list":case_write_list
                     }
        return ApiResponse(results=count_all)

class ProjectViewsets(ModelViewSet):
    """
        retrieve:
            返回一个项目（查）
        list:
            返回所有项目（查）
        create:
            创建项目（增）
        delete:
            删除项目（删）
        partial_update:
            更新现有组中的一个或多个字段（改：部分更改)
        update:
            更新项目（改）
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = CustomPagination
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [MyPermission]

    #通过name模糊筛选
    @action(methods=['get'],detail=False)
    def query_name(self, request, *args,**kwargs):
        project_name_type = Project.objects.filter(name__contains=self.request.query_params.get('name','')).filter(type__contains=self.request.query_params.get('type',''))
        ser = ProjectSerializer(project_name_type,many=True)
        return ApiResponse(results=ser.data, status=status.HTTP_200_OK)

class HostViewSets(ModelViewSet):
    """
        retrieve:
            返回一个host（查）
        list:
            返回所有host（查）
        create:
            创建host（增）
        delete:
            删除host（删）
        partial_update:
            更新现有组中的一个或多个字段（改：部分更改)
        update:
            更新host（改）
    """
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    pagination_class = CustomPagination
    permission_classes = [MyPermission]
    authentication_classes = [CustomJSONWebTokenAuthentication]
    #通过name筛选
    @action(methods=['get'],detail=False)
    def query_name(self, request, *args,**kwargs):
        host_name = Host.objects.filter(name__contains=self.request.query_params.get("name"))
        ser = HostSerializer(host_name,many=True)
        return ApiResponse(results=ser.data)

class ApiViewsets(APIModelViewSet):
    """
        retrieve:
            返回一个api（查）
        list:
            返回所有api（查）
        create:
            创建api（增）
        delete:
            删除api（删）
        partial_update:
            更新现有组中的一个或多个字段（改：部分更改)
        update:
            更新api（改）
    """
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
    pagination_class = CustomPagination
    permission_classes = [MyPermission]
    authentication_classes = [CustomJSONWebTokenAuthentication]
    # def get_queryset(self):
    #     try:
    #         return self.queryset.filter(path__contains=self.request.query_params.get('path', '')).filter(project_id=self.request.query_params.get('project_id'))
    #     except Exception as e:
    #         return self.queryset.filter(path__contains=self.kwargs.get('path'))

class RunApiRecordAPIView(APIView):
    """
    运行api
    """
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [MyPermission]

    def post(self, request, api_id):
        api = Api.objects.get(pk=api_id)
        # 添加用例参数
        case_arguments = ApiArgument.objects.filter(api=api)
        global_arguments = {}
        for case_argument in case_arguments:
            global_arguments[case_argument.name] = case_argument.value
        logger.info("API{}的全局参数:{}".format(api, global_arguments))
        api_res = apiRequest(api,global_arguments)
        res = api_res[0]
        # 断言结果(断言状态和内容)
        # 断言状态码，如果状态码不一致，直接失败
        logger.info("预期状态码:{},响应状态码:{}".format(res.status_code,api.expect_code))
        # if res.status_code == int(api.expect_code):
        #     #判断是否为空
        #     if len(api.expect_content)>1:
        #         expect_content = api.expect_content
        #         expect_content_key = expect_content.split("=")[0]
        #         expect_content_value = expect_content.split("=")[1]
        #         # 断言内容
        #         logger.info("断言内容的key:{}".format(dictor(res.json(), expect_content_key)))
        #         logger.info("断言内容的value:{}".format(expect_content_value))
        #         if dictor(res.json(), expect_content_key) == expect_content_value:
        #             # 断言成功
        #             assert_result = "pass"
        #         else:
        #             logger.info("断言内容失败")
        #             assert_result = "fail"
        #     else:
        #         assert_result = "pass"
        # else:
        #     logger.info("状态码断言失败")
        #     assert_result = "fail"
        remarks= []
        if res.status_code == int(api.expect_code):
            # 断言内容
            if api.expect_content:
                # 遍历断言内容
                for assert_content in literal_eval(api.expect_content):
                    for key, value in assert_content.items():
                        actual_value = key
                        assert_value = dictor(res.json(), value)
                        # 每个内容断言确认
                        if actual_value == assert_value:
                            assert_result = "pass"
                        else:
                            assert_result = "fail"
                            remarks.append(
                                "断言内容不一致，响应数据提取内容:{},预期内容:{},实际内容:{}".format(assert_content, assert_value,
                                                                             actual_value))
                            logger.error("断言内容不一致，预期内容:{},实际内容:{}".format(assert_value, actual_value))
                            break
            else:
                assert_result = "pass"
        # 状态码不一致
        else:
            assert_result = "fail"
        logger.info("api结果:{}".format(assert_result))
        #保存运行记录
        record = RunApiRecord.objects.create(
            name = api.name,
            url=res.url,
            http_method=res.request.method,
            return_code=res.status_code,
            return_content=res.text,
            data=api_res[1],
            headers=api.headers,
            api=api,
            assert_result=assert_result
        )
        serializer = RunApiRecordSerializer(record).data
        return ApiResponse(results=serializer)

# class CaseImport(APIView):
#     """
#     导入excel的测试用例
#     """
#     def post(self,request):
#         try:
#             with transaction.atomic():
#                 f = request.FILES.get('excel_file')
#                 if f:
#                     wb = xlrd.open_workbook(filename=None, file_contents=f.read())
#                     table = wb.sheets()[0]
#                     rows = table.nrows
#                     for i in range(1, rows):
#                         row = table.row_values(i)
#                         host_id = Host.objects.filter(modular=row[1]).first().id
#                         project_id = Project.objects.filter(name=row[8]).first().id
#                         case = ChanDaoCase.objects.create(modular_id=modular_id,
#                                                           title=row[2],
#                                                           preconditions=row[3],
#                                                           case_type=row[4],
#                                                           case_stage=row[5],
#                                                           case_priority=row[6],
#                                                           remarks=row[7],
#                                                           user_id=user_id,
#                                                           result="unexecuted")
#                         ChanDaoCaseStep.objects.create(step=row[12],expect=row[13],case_result="unexecuted",remarks="",case=case)
#         except Exception as e:
#             return ApiResponse(status=1, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR, msg="错误",results="导入失败，第{}行数据异常---{}".format(i,e))
#         return ApiResponse(results="导入成功")


class ApiDumpView(DataDumpView):
    """导出订单详情"""
    model = Api
    fields = '__all__'
    method_fields = {'api_argument': '全局参数','api_argument_extract':'参数提取'} # 获取这个值需要自己实现get__sign方法
    exclude = [] # 导出时排除的字段
    order_field = '-create_time'
    sheet_size = 500
    file_name = '测试用例'
    permission_classes = []


    def get_queryset(self, request):
        """从request中获取参数进行筛选"""
        return super().get_queryset(request)

    def get__api_argument(self, obj):
        """
        全局参数
        :param obj:
        :return:
        """
        api_arguments = ApiArgument.objects.filter(api=obj)
        len_api_arguments = ApiArgument.objects.filter(api=obj).count()
        api_argument_result = []
        #如果没有数据，excel显示空
        if len_api_arguments == 0:
            return None
        else:
            for api_argument in range(len_api_arguments):
                api_argument_result.append({"name":api_arguments[api_argument].name,"value":api_arguments[api_argument].value})
        return str(api_argument_result)


    def get__api_argument_extract(self, obj):
        """
        参数提取
        :param obj:
        :return:
        """
        api_argument_extracts = ApiArgumentExtract.objects.filter(api=obj)
        len_api_argument_extracts = ApiArgumentExtract.objects.filter(api=obj).count()
        api_argument_extract_result = []
        if len_api_argument_extracts == 0:
            return None
        else:
            for api_argument_extract in range(len_api_argument_extracts):
                api_argument_extract_result.append({"name":api_argument_extracts[api_argument_extract].name,"origin":api_argument_extracts[api_argument_extract].origin,"format":api_argument_extracts[api_argument_extract].format})
        return str(api_argument_extract_result)

class ParameterizationViewSet(ModelViewSet):
    """
    参数化表达式
    """
    queryset = Parameterization.objects.all()
    pagination_class = CustomPagination
    serializer_class = ParameterizationSerializer


