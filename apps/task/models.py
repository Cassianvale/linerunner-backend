from django.db import models

# Create your models here.
from django.db import models
import datetime
from django.db.backends.mysql.base import DatabaseWrapper

DatabaseWrapper.data_types = DatabaseWrapper.data_types
class TestTask(models.Model):
    """
    测试任务
    """
    month = models.CharField(max_length=20,verbose_name="月份")
    task_name = models.CharField(max_length=200,verbose_name="任务标题")
    tester = models.CharField(max_length=50,null=True, verbose_name="测试人员")
    develop = models.CharField(max_length=50,null=True, verbose_name="开发人员")
    start_time = models.CharField(max_length=50,null=True,verbose_name="测试开始时间")
    end_time = models.CharField(max_length=50,null=True,blank=True,verbose_name="测试结束时间")
    publish_time = models.CharField(max_length=200,null=True,blank=True,verbose_name="发版时间")
    class Meta:
        db_table = "test_task"
        verbose_name = "测试任务表"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.task_name

class CrontabTask(models.Model):
    """
    定时任务模型
    1. 定时执行API
    2. 定时执行用例
    3. 定时执行测试集

    任务触发方式：date,interval,crontab
    我们用crontab的表达式
    需要用json的格式："{"second":"*/1","hour":"12"}"
    先将这个json load成字典
    dict = json.loads(json_str)
    dict = {"second":"*/1","hour":"12"}
    scheduler.add_job(func,trigger="cron",second="*/1",hour="12")
    scheduler.add_job(func,trigger="cron",**dict)
    """
    CRONTAB_TASK_STATUS = (
        (1, 1),  # 运行
        (2, 2),  # 停止
    )

    name = models.CharField(max_length=100,verbose_name='任务名称')
    case_id = models.CharField(max_length=500,verbose_name='定时执行的用例')
    create_time = models.DateTimeField(auto_now=True,verbose_name='创建时间')
    expr = models.CharField(max_length=200,verbose_name='任务执行表达式')
    status = models.SmallIntegerField(choices=CRONTAB_TASK_STATUS,verbose_name='任务的状态',default=2)

    class Meta:
        db_table = "crontab_task"
        verbose_name = "定时任务"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name