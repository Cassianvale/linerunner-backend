from django.db import models
from apps.apiTest.models import Project
# Create your models here.
class XmFileModel(models.Model):
    name = models.CharField(max_length=50, verbose_name="文件名称")
    path = models.CharField(max_length=300, verbose_name="oss文件地址")
    create_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    suffix_name = models.CharField(max_length=50, verbose_name="文件名称")
    project= models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='关联的项目', null=True)
    class Meta:
        ordering = ['-create_time']
        db_table = "linerunner_xm_file"
        verbose_name="xmind文件"
        verbose_name_plural=verbose_name
    def __str__(self):
        return "{}".format(self.name)
