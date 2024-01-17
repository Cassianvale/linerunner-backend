# -*-coding:utf-8 -*-

from django.db import models
from ..apiTest.models import Api


class Case(models.Model):
    """
    自动化测试用例
    """
    name = models.CharField(max_length=50, verbose_name='用例名称')
    # api_list = models.ManyToManyField(Api,related_name='case_list',through='CaseApiList')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    create_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = "case"
        verbose_name = "自动化测试用例"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.name)


class CaseApiList(models.Model):
    """
    case中的api_list
    """
    api = models.ForeignKey(Api, on_delete=models.CASCADE, null=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True, related_name='api_list')
    # 添加的字段
    index = models.IntegerField(verbose_name="执行顺序", null=True)
    reset_data = models.TextField(null=True, blank=True, verbose_name='提交的数据')
    reset_expect_content = models.CharField(null=True, max_length=200, verbose_name='期望返回的内容', blank=True)
    reset_expect_code = models.CharField(null=True, max_length=200, verbose_name='预期状态码', blank=True)

    class Meta:
        managed = True
        db_table = "case_api_list"
        verbose_name = "测试用例中的api"
        verbose_name_plural = verbose_name


class CaseRunRecord(models.Model):
    """
    用例运行记录
    """
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name='所属用例')
    create_time = models.DateTimeField(auto_now=True, verbose_name='运行时间')

    class Meta:
        ordering = ['-create_time']
        db_table = "case_run_record"
        verbose_name = "用例运行记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.case)


class CaseApiRunRecord(models.Model):
    """
    Case API运行记录
    """
    HTTP_METHOD_CHOICE = (
        ('POST', 'POST'),
        ('GET', 'GET'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE')
    )

    name = models.CharField(max_length=200, verbose_name='api名称')
    url = models.CharField(max_length=200, verbose_name='请求的url！')
    http_method = models.CharField(max_length=10, verbose_name='请求方式', choices=HTTP_METHOD_CHOICE)
    headers = models.TextField(null=True, verbose_name='请求头')
    data = models.TextField(null=True, verbose_name='提交的数据')
    create_time = models.DateTimeField(auto_now=True, verbose_name='运行的时间')
    return_code = models.CharField(max_length=10, verbose_name='响应状态码')
    return_content = models.TextField(null=True, verbose_name='响应内容')
    return_time = models.CharField(max_length=1000, verbose_name='响应时间')
    api = models.ForeignKey(Api, on_delete=models.CASCADE, verbose_name='关联的API', null=True)
    case_record = models.ForeignKey(CaseRunRecord, on_delete=models.CASCADE, verbose_name='关联的case_record',
                                    related_name='api_records')

    class Meta:
        db_table = "case_api_run_record"
        verbose_name = "Case API运行记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.url)
