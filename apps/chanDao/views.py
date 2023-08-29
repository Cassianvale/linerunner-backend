from django.shortcuts import render
import xlrd
import os
from utils.excel import DataDumpView
from .models import ChanDaoCase,ChanDaoProject,ChanDaoModular,ChanDaoCaseStep
from .serializers import ChanDaoCaseSerializer,ChanDaoProjectSerializer,ChanDaoModularSerializer,ChanDaoCaseStepSerializer
from ..users.authorizations import JWTAuthentication
from ..users.permission import MyPermission
from ..users.models import Users
from utils.pagination import MyPageNumberPagination
from utils.apiResponse import ApiResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from lwjTest.settings import logger
from django.db import transaction
from utils.primordial_sql import my_custom_sql
from rest_framework import status
from django.http import FileResponse
class ChanDaoProjectViewSet(ModelViewSet):
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
    queryset = ChanDaoProject.objects.all()
    serializer_class = ChanDaoProjectSerializer
    pagination_class = MyPageNumberPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [MyPermission]
    def get_queryset(self):
        """
        统计每个项目的模块总数量
        :return:
        """
        if self.request.method=='GET':
            project_all = ChanDaoProject.objects.all()
            for project in project_all:
                #查询该项目下的模块的总数量
                project.modular_count = ChanDaoModular.objects.filter(project_id=project.id).count()
            return project_all
        return ChanDaoProject.objects.all()

class ChanDaoModularViewSet(ModelViewSet):
    """
        retrieve:
            返回一个模块（查）
        list:
            返回所有模块（查）
        create:
            创建模块（增）
        delete:
            删除模块（删）
        partial_update:
            更新现有组中的一个或多个字段（改：部分更改)
        update:
            更新模块（改）
    """
    queryset = ChanDaoModular.objects.all()
    serializer_class = ChanDaoModularSerializer
    pagination_class = MyPageNumberPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [MyPermission]
    def project_modular(self,request,project_id=None):
        """
        获取某个项目下的模块列表
        :param request:
        :param project_id:
        :return:
        """
        modular_all = ChanDaoModular.objects.filter(project_id=project_id)
        for modular in modular_all:
            #查询该项目下的模块的总数量
            modular.case_count = ChanDaoCase.objects.filter(modular_id=modular.id).count()
            modular.case_unexecuted_count = ChanDaoCase.objects.filter(modular_id=modular.id,result='unexecuted').count()
            modular.case_pass_count = ChanDaoCase.objects.filter(modular_id=modular.id,result='pass').count()
            modular.case_fail_count = ChanDaoCase.objects.filter(modular_id=modular.id,result='fail').count()
            modular.case_block_count = ChanDaoCase.objects.filter(modular_id=modular.id,result='block').count()
        pg = MyPageNumberPagination()
        page_modular = pg.paginate_queryset(queryset=modular_all, request=request, view=self)
        ser = ChanDaoModularSerializer(instance=page_modular,many=True).data
        return pg.get_paginated_response(ser)

    def get_queryset(self):
        """
        统计模块下的用例状态
        :return:
        """
        if self.request.method=='GET':
            modular_all = ChanDaoModular.objects.all()
            for modular in modular_all:
                #查询该项目下的模块的总数量
                modular.case_count = ChanDaoCase.objects.filter(modular_id=modular.id).count()
                modular.case_unexecuted_count = ChanDaoCase.objects.filter(modular_id=modular.id,result='unexecuted').count()
                modular.case_pass_count = ChanDaoCase.objects.filter(modular_id=modular.id,result='pass').count()
                modular.case_fail_count = ChanDaoCase.objects.filter(modular_id=modular.id,result='fail').count()
                modular.case_block_count = ChanDaoCase.objects.filter(modular_id=modular.id,result='block').count()
            return modular_all
        return ChanDaoModular.objects.all()

class ChanDaoCaseViewSet(ModelViewSet):
    """
        retrieve:
            返回一个用例（查）
        list:
            返回所有用例（查）
        create:
            创建用例（增）
        delete:
            删除用例（删）
        partial_update:
            更新现有组中的一个或多个字段（改：部分更改)
        update:
            更新用例（改）
    """
    queryset = ChanDaoCase.objects.all()
    serializer_class = ChanDaoCaseSerializer
    pagination_class = MyPageNumberPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [MyPermission]

    def modular_case(self,request,modular_id=None):
        """
        获取项目下的模块数据
        :param request:
        :param modular_id:
        :return:
        """
        case_list = ChanDaoCase.objects.filter(modular_id=modular_id)
        pg = MyPageNumberPagination()
        page_case = pg.paginate_queryset(queryset=case_list, request=request, view=self)
        ser = ChanDaoCaseSerializer(instance=page_case,many=True).data
        return pg.get_paginated_response(ser)

class CaseResult(APIView):
    """
    用例的步骤
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [MyPermission]
    def get(self, request, case_id=None):
        """
        获取用例的步骤
        :param request:
        :param case_id: 用例id
        :return:
        """
        caseResult = ChanDaoCaseStep.objects.filter(case_id=case_id)
        ser = ChanDaoCaseStepSerializer(instance=caseResult,many=True).data
        return Response(ser)

    def put(self, request, case_id=None):
        """
        更新用例的结果
        :param request:
        :param case_id: 用例id
        :return:
        """
        request_data = request.data
        for id,case_result in enumerate(request_data):
            result_obj = ChanDaoCaseStep.objects.filter(case_id=case_id)[id]
            ser = ChanDaoCaseStepSerializer(data=case_result,instance=result_obj)
            if ser.is_valid():
                ser.save()
        #如果用例有阻塞或者失败的，则返回失败
        case_step = ChanDaoCaseStep.objects.filter(case_id=case_id)
        case = ChanDaoCase.objects.get(pk=case_id)
        #用例下的所有步骤的状态
        case_result_list = []
        for case_result in case_step:
            case_result_list.append(case_result.case_result)
        #case标记失败
        if 'fail' in case_result_list:
            case.result='fail'
            case.save()
        #case标记成功
        elif 'fail' and 'unexecuted' not in case_result_list:
            case.result = 'pass'
            case.save()
        #case标记未执行
        elif 'fail' and 'pass' not in case_result_list:
            case.result = 'unexecuted'
            case.save()
        return Response("更新成功")

class DataCountView(APIView):
    """
    数据统计
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [MyPermission]
    def get(self, request):
        #总的项目
        project_count = ChanDaoProject.objects.all().count()
        #总的模块
        modular_count = ChanDaoModular.objects.all().count()
        #总的用例
        case_count = ChanDaoCase.objects.all().count()
        #项目下用例数量
        sql="SELECT " \
                "c.project," \
                "count(e.id) as count_id " \
            "FROM	" \
                "fusion_chandao_project c	" \
                "LEFT JOIN fusion_chandao_modular d ON c.id = d.project_id 	" \
                "LEFT JOIN fusion_chandao_case e ON d.id = e.modular_id  " \
            "GROUP BY c.project"
        sql_result = my_custom_sql(sql)
        #项目的用例统计
        data=[]
        for project in sql_result:
            project_data = {}
            project_data['project']=project[0]
            project_data['case_count']=project[1]
            data.append(project_data)
        #数据整理
        chandao_data = {
            "project_count":project_count,
            "modular_count":modular_count,
            "case_count":case_count,
            "data":data,
        }
        return ApiResponse(results=chandao_data)

class CaseImport(APIView):
    """
    导入excel的测试用例
    """
    def post(self,request):
        try:
            with transaction.atomic():
                f = request.FILES.get('excel_file')
                if f:
                    wb = xlrd.open_workbook(filename=None, file_contents=f.read())
                    table = wb.sheets()[0]
                    rows = table.nrows
                    for i in range(1, rows):
                        row = table.row_values(i)
                        modular_id = ChanDaoModular.objects.filter(modular=row[1]).first().id
                        user_id = Users.objects.filter(name=row[8]).first().id
                        case = ChanDaoCase.objects.create(modular_id=modular_id,
                                                          title=row[2],
                                                          preconditions=row[3],
                                                          case_type=row[4],
                                                          case_stage=row[5],
                                                          case_priority=row[6],
                                                          remarks=row[7],
                                                          user_id=user_id,
                                                          result="unexecuted")
                        ChanDaoCaseStep.objects.create(step=row[12],expect=row[13],case_result="unexecuted",remarks="",case=case)
        except Exception as e:
            return ApiResponse(status=1, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR, msg="错误",results="导入失败，第{}行数据异常---{}".format(i,e))
        return ApiResponse(results="导入成功")

class CaseDumpView(DataDumpView):
    """导出订单详情"""
    model = ChanDaoCase
    fields = '__all__'
    method_fields = {'step': '步骤','expect':'预期'} # 获取这个值需要自己实现get__sign方法
    # exclude = ['id'] # 导出时排除的字段
    order_field = '-found_time'
    sheet_size = 500
    file_name = '测试用例'
    permission_classes = []


    def get_queryset(self, request):
        """从request中获取参数进行筛选"""
        return super().get_queryset(request)

    def get__step(self, obj):
        """
        步骤
        :param obj:
        :return:
        """
        steps = ChanDaoCaseStep.objects.filter(case=obj)
        len_steps = ChanDaoCaseStep.objects.filter(case=obj).count()
        step_result = ""
        for index in range(len_steps):
            step_result+=str(index+1)+":"+str(steps[index].step)
            if (index+1)!=len_steps:
                step_result+='\n'
        return step_result

    def get__expect(self, obj):
        """
        预期内容
        :param obj:
        :return:
        """
        expects = ChanDaoCaseStep.objects.filter(case=obj)
        len_expects = ChanDaoCaseStep.objects.filter(case=obj).count()
        expect_result = ""
        for index in range(len_expects):
            expect_result += str(index + 1) + ":" + str(expects[index].expect)
            if (index + 1) != len_expects:
                expect_result += '\n'
        return expect_result

    # def get__users(self, obj):
    #     """
    #     创建人
    #     :param obj:
    #     :return:
    #     """
    #     user = Users.objects.get(id=obj.user_id).name
    #     return str(user)


class CaseDumpTemplateView(DataDumpView):
    """导出模版详情"""
    model = ChanDaoCase
    fields = '__all__'
    method_fields = {'step': '步骤','expect':'预期'} # 获取这个值需要自己实现get__sign方法
    exclude = ['id'] # 导出时排除的字段
    order_field = ''
    sheet_size = 300
    file_name = '测试用例'
    permission_classes = []

    def get__step(self, obj):
        """
        步骤
        :param obj:
        :return:
        """
        return ""

    def get__expect(self, obj):
        """
        预期结果
        :param obj:
        :return:
        """
        return ""

class ExcelDownload(APIView):
    """测试使用django-excel下载文件"""

    def get(self,request):
        BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(BASE_DIR, "../templates/测试用例.xls")
        # path = os.path.join(BASE_DIR, "../file/2.jpg")
        file_name = "测试用例.xls"
        file = open(path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name).encode()
        return response

