from django.db import models
from ..user.models import BaseTable
from django.contrib.auth import get_user_model
from django.conf import settings

users = get_user_model()


class Project(BaseTable):
    """
    项目管理
    """

    PROJECTTYPE = [
        ['web', 'web'],
        ['app', 'app']
    ]

    name = models.CharField(max_length=50, verbose_name='项目名称')
    type = models.CharField(max_length=50, verbose_name='项目类型', choices=PROJECTTYPE)
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='项目描述')
    create_user = models.ForeignKey(users, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='创建人')
    product_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, verbose_name="产品负责人")
    test_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, verbose_name="测试负责人")

    class Meta:
        db_table = 'project'
        verbose_name = "项目管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.name)


class Modular(BaseTable):
    """
    模块管理
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    modular = models.CharField(max_length=20, verbose_name="模块名称")

    class Meta:
        db_table = "modular"
        verbose_name = "模块管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.modular)


class Host(BaseTable):
    """
    环境变量
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目', related_name='host_list')
    name = models.CharField(max_length=50, verbose_name='环境名称')
    host = models.CharField(max_length=1024, verbose_name='Host域名(前置URL)')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')

    class Meta:
        db_table = "host"
        verbose_name = "环境变量"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.host)




