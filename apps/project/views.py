import datetime
from rest_framework import status
from utils.primordial_sql import my_custom_sql
from .models import Project, Host, Modular
from .serializers import ProjectSerializer, HostSerializer, ModularSerializer
from ..test.models import TestCase, TestCaseStep
from utils.apiResponse import ApiResponse
from utils.pagination import CustomPagination
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from ..apiTest.models import Api
from ..case.models import Case
from ..user.authentications import CustomJSONWebTokenAuthentication
from ..user.permission import MyPermission

users = get_user_model()


class ProjectViewSet(ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = CustomPagination
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [MyPermission]

    def get_queryset(self):
        """
        统计每个项目的模块总数量
        """

        if self.request.method == 'GET':
            project_all = Project.objects.all()
            for project in project_all:
                # 查询该项目下的模块的总数量
                project.modular_count = Modular.objects.filter(project_id=project.id).count()
            return project_all
        return Project.objects.all()

    def get_serializer_class(self):
        # 通过name模糊筛选
        @action(methods=['get'], detail=False)
        def query_name(self, request, *args, **kwargs):
            project_name_type = Project.objects.filter(name__contains=self.request.query_params.get('name', '')).filter(
                type__contains=self.request.query_params.get('type', ''))
            ser = ProjectSerializer(project_name_type, many=True)
            return ApiResponse(results=ser.data, status=status.HTTP_200_OK)


class ModularViewSet(ModelViewSet):

    queryset = Modular.objects.all()
    serializer_class = ModularSerializer
    pagination_class = CustomPagination
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [MyPermission]

    def project_modular(self, request, project_id=None):
        """
        获取某个项目下的模块列表
        """

        modular_all = Modular.objects.filter(project_id=project_id)
        for modular in modular_all:
            # 查询该项目下的模块的总数量
            modular.case_count = TestCase.objects.filter(modular_id=modular.id).count()
            modular.case_unexecuted_count = TestCase.objects.filter(modular_id=modular.id,
                                                                       result='unexecuted').count()
            modular.case_pass_count = TestCase.objects.filter(modular_id=modular.id, result='pass').count()
            modular.case_fail_count = TestCase.objects.filter(modular_id=modular.id, result='fail').count()
            modular.case_block_count = TestCase.objects.filter(modular_id=modular.id, result='block').count()
        pg = CustomPagination()
        page_modular = pg.paginate_queryset(queryset=modular_all, request=request, view=self)
        ser = ModularSerializer(instance=page_modular, many=True).data
        return pg.get_paginated_response(ser)

    def get_queryset(self):
        """
        统计模块下的用例状态
        """
        if self.request.method == 'GET':
            modular_all = Modular.objects.all()
            for modular in modular_all:
                # 查询该项目下的模块的总数量
                modular.case_count = TestCase.objects.filter(modular_id=modular.id).count()
                modular.case_unexecuted_count = TestCase.objects.filter(modular_id=modular.id,
                                                                           result='unexecuted').count()
                modular.case_pass_count = TestCase.objects.filter(modular_id=modular.id, result='pass').count()
                modular.case_fail_count = TestCase.objects.filter(modular_id=modular.id, result='fail').count()
                modular.case_block_count = TestCase.objects.filter(modular_id=modular.id, result='block').count()
            return modular_all
        return Modular.objects.all()


class HostViewSets(ModelViewSet):
    """
    环境变量
    """
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    pagination_class = CustomPagination
    permission_classes = [MyPermission]
    authentication_classes = [CustomJSONWebTokenAuthentication]

    # 通过name筛选
    @action(methods=['get'], detail=False)
    def query_name(self, request, *args, **kwargs):
        host_name = Host.objects.filter(name__contains=self.request.query_params.get("name"))
        ser = HostSerializer(host_name, many=True)
        return ApiResponse(results=ser.data)


# class DataCountView(APIView):
#     """
#     项目管理数据统计
#     """
#     permission_classes = [MyPermission]
#     authentication_classes = [CustomJSONWebTokenAuthentication]
#
#     def get(self, request):
#         # 基础数据"总项目数，总域名，总接口数，总用例数"
#         project_count = Project.objects.count()
#         host_count = Host.objects.count()
#         api_count = Api.objects.count()
#         case_count = Case.objects.count()
#         # 总自动化用例近5天编写情况
#         api_write_list = []
#         case_write_list = []
#         for day in range(5):
#             threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days=day))
#             otherStyleTime = threeDayAgo.strftime("%Y-%m-%d")
#             # api近5日编写统计情况
#             api_counts = Api.objects.filter(create_time__contains=otherStyleTime).count()
#             api_write_list.append({"time": otherStyleTime, "api_count": api_counts})
#             # case近5日编写统计情况
#             case_counts = Case.objects.filter(create_time__contains=otherStyleTime).count()
#             case_write_list.append({"time": otherStyleTime, "case_count": case_counts})
#         count_all = {"project_count": project_count,
#                      "host_count": host_count,
#                      "api_count": api_count,
#                      "case_count": case_count,
#                      "api_write_list": api_write_list,
#                      "case_write_list": case_write_list
#                      }
#         return ApiResponse(results=count_all)


class DataCountView(APIView):
    """
    数据统计
    """
    authentication_classes = [CustomJSONWebTokenAuthentication]
    permission_classes = [MyPermission]

    def get(self, request):
        # 总的项目
        project_count = Project.objects.all().count()
        # 总的模块
        modular_count = Modular.objects.all().count()
        # 总的用例
        case_count = TestCase.objects.all().count()
        # 项目下用例数量
        sql = "SELECT " \
              "c.project," \
              "count(e.id) as count_id " \
              "FROM	" \
              "project c	" \
              "LEFT JOIN modular d ON c.id = d.project_id 	" \
              "LEFT JOIN testcase e ON d.id = e.modular_id  " \
              "GROUP BY c.project"
        sql_result = my_custom_sql(sql)
        # 项目的用例统计
        data = []
        for project in sql_result:
            project_data = {'project': project[0], 'case_count': project[1]}
            data.append(project_data)
        # 数据整理
        chandao_data = {
            "project_count": project_count,
            "modular_count": modular_count,
            "case_count": case_count,
            "data": data,
        }
        return ApiResponse(results=chandao_data)


class DataCountView(APIView):
    """
    项目管理数据统计
    """
    permission_classes = [MyPermission]
    authentication_classes = [CustomJSONWebTokenAuthentication]

    def get(self, request):
        # 基础数据"总项目数，总域名，总接口数，总用例数"
        project_count = Project.objects.count()
        host_count = Host.objects.count()
        api_count = Api.objects.count()
        case_count = Case.objects.count()
        # 总自动化用例近5天编写情况
        api_write_list = []
        case_write_list = []
        for day in range(5):
            threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days=day))
            otherStyleTime = threeDayAgo.strftime("%Y-%m-%d")
            # api近5日编写统计情况
            api_counts = Api.objects.filter(create_time__contains=otherStyleTime).count()
            api_write_list.append({"time": otherStyleTime, "api_count": api_counts})
            # case近5日编写统计情况
            case_counts = Case.objects.filter(create_time__contains=otherStyleTime).count()
            case_write_list.append({"time": otherStyleTime, "case_count": case_counts})
        count_all = {"project_count": project_count,
                     "host_count": host_count,
                     "api_count": api_count,
                     "case_count": case_count,
                     "api_write_list": api_write_list,
                     "case_write_list": case_write_list
                     }
        return ApiResponse(results=count_all)


