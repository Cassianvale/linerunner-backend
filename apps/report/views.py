# -*-coding:utf-8 -*-
from django.conf.global_settings import EMAIL_HOST_USER
from django.shortcuts import render
from .models import ReportModel, EmailModel
from ..user.authentications import CustomJSONWebTokenAuthentication
from ..user.permission import MyPermission
from rest_framework.views import APIView
from .serializers import ReportModelSerializer, EmailSerializer
from utils.apiResponse import ApiResponse
from utils.pagination import CustomPagination
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from django.core import mail
from linerunner.settings import *
from utils.modelViewSet import APIModelViewSet


class ReportVIew(APIView):
    """
    报告列表
    """

    def get(self, request, *args, **kwargs):
        # 查询数据库中未被删除的报告对象
        # report_obj = ReportModel.objects.filter(is_delete=False)
        # 对查询结果进行序列化
        # serailizer = ReportModelSerializer(report_obj,many=True)
        # return ApiResponse(results=serailizer.data)
        report_obj = ReportModel.objects.filter(is_delete=False)
        pg = CustomPagination()
        page_report = pg.paginate_queryset(queryset=report_obj, request=request, view=self)
        ser = ReportModelSerializer(instance=page_report, many=True).data
        return pg.get_paginated_response(ser)

    def delete(self, request, id=None):
        report_obj = ReportModel.objects.get(pk=id)
        report_obj.is_delete = True
        report_obj.save()
        return ApiResponse(results="删除成功")


class EmailViewSet(APIModelViewSet):
    """
    邮箱列表
    """
    queryset = EmailModel.objects.all()
    pagination_class = CustomPagination
    serializer_class = EmailSerializer


def reportDetails(request, name=None):
    """
    报告详情
    :param request:
    :param name:
    :return:
    """
    return render(request, "report/{}".format(name))


def testMail():
    """
    配置
    :return:
    """
    report = ReportModel.objects.filter().order_by('-id')[:1]
    html = '''
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
    <p>本邮件由系统自动发出，无需回复！</p><br>
    <p></p>
            <ul>
                <li><span><b>报告名称：</b></span><input type="text" value="{}"></li></b>
                <li><span><b>用例总数：</b></span><input type="text" value="{}"></li></b>
                <li><span><b>用例通过：</b></span><input type="text" value="{}"></li></b>
                <li><span class="error"><b>用例失败：</b></span><input type="text" value="{}"></li></b>
                <li><span class="warning"><b>用例跳过：</b></span><input type="text" value="0"></li></b>
                <li><span class="add"><b>报告地址：</b></span><a href="{}"><input type=button value="点击进入测试报告详情"></a></li>
            </ul>
    </body>
    </html>
    '''.format(report[0].project_name,
               report[0].case_all,
               report[0].case_pass,
               report[0].case_fail,
               report[0].report_details)
    # 收件人列表
    recipient_list = [e.email for e in EmailModel.objects.filter(status=True)]
    print(recipient_list)
    from_mail = EMAIL_HOST_USER

    title = "linerunner接口测试报告"
    msg = mail.EmailMessage(title, html, from_mail, recipient_list)
    msg.content_subtype = 'html'
    msg.encoding = 'utf-8'
    if msg.send():
        return True
    else:
        return False


def mailReport(request, name=None):
    """
    发送邮件
    :param request:
    :return:
    """
    report = ReportModel.objects.filter(project_name=name).first()
    context = {
        "project_name": report.project_name,
        "case_all": report.case_all,
        "case_pass": report.case_pass,
        "case_fail": report.case_fail,
        "report_details": report.report_details,
    }
    if testMail():
        return render(request, template_name="report.html", context=context)
    else:
        return render(request, template_name="error.html")
