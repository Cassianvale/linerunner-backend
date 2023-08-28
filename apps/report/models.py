# -*-coding:utf-8 -*-

from django.db import models


class ReportModel(models.Model):
    """
    测试报告
    """
    PROJECT_URL_CHOICES = [
        ["开发环境","开发环境"],
        ["测试环境","测试环境"],
        ["线上环境","线上环境"]
    ]
    PROJECT_TYPE = [
    ["ui","ui"],
    ["接口","接口"]
    ]
    project_name = models.CharField(max_length=100,verbose_name="项目名称")
    project_host = models.CharField(choices=PROJECT_URL_CHOICES,max_length=100,default=None,null=True,blank=True,verbose_name="用例执行环境")
    case_type= models.CharField(choices=PROJECT_TYPE,max_length=100,default=1,verbose_name="用例类型")
    case_all=models.IntegerField(verbose_name="用例总数")
    case_pass=models.IntegerField(verbose_name="用例成功次数")
    case_fail=models.IntegerField(verbose_name="用例失败次数")
    start_time=models.CharField(max_length=100,verbose_name="开始时间")
    run_time = models.CharField(max_length=100,verbose_name="运行时间")
    report_details = models.CharField(max_length=300,verbose_name="报告详情")
    is_delete= models.BooleanField(default=False,verbose_name="是否删除")
    create_time= models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    class Meta:
        ordering = ['-create_time']
        db_table = "linerunner_report"
        verbose_name = "报告表"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.project_name

class EmailModel(models.Model):
    email = models.CharField(max_length=100,verbose_name="邮箱地址")
    name = models.CharField(max_length=100,verbose_name="姓名")
    status = models.BooleanField(default=True,verbose_name="是否禁用")

    class Meta:
        db_table = "linerunner_email"
        verbose_name = "邮箱表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email



