from django.db import models
from django.contrib.auth import get_user_model

users = get_user_model()


class ChanDaoProject(models.Model):
    """
    项目名称
    """
    project = models.CharField(max_length=30, verbose_name="项目名称")
    product_person = models.CharField(max_length=20, verbose_name="产品负责人")
    test_person = models.CharField(max_length=20, verbose_name="测试负责人")

    class Meta:
        db_table = "chandao_project"
        verbose_name = "项目名称"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.project)


class ChanDaoModular(models.Model):
    """
    禅道-模块
    """
    project = models.ForeignKey(ChanDaoProject, on_delete=models.CASCADE)
    modular = models.CharField(max_length=20, verbose_name="模块名称")

    class Meta:
        db_table = "chandao_modular"
        verbose_name = "禅道_项目模块"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.modular)


