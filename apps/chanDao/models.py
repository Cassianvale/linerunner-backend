from django.db import models
from django.contrib.auth import get_user_model
users = get_user_model()



class ChanDaoProject(models.Model):
    """
    阐道-项目名称
    """
    project = models.CharField(max_length=30,verbose_name="项目名称")
    product_person = models.CharField(max_length=20, verbose_name="产品负责人")
    test_person = models.CharField(max_length=20, verbose_name="测试负责人")
    class Meta:
        db_table = "fusion_chandao_project"
        verbose_name="阐道_项目名称"
        verbose_name_plural=verbose_name
        ordering = ['id']
    def __str__(self):
        return "{}".format(self.project)

class ChanDaoModular(models.Model):
    """
    阐道-模块
    """
    project = models.ForeignKey(ChanDaoProject,on_delete=models.CASCADE)
    modular = models.CharField(max_length=20,verbose_name="模块名称")
    class Meta:
        db_table = "fusion_chandao_modular"
        verbose_name="阐道_项目模块"
        verbose_name_plural=verbose_name
    def __str__(self):
        return "{}".format(self.modular)

class ChanDaoCase(models.Model):
    """
    阐道-用例
    """
    CASE_TYPE = [
        ['功能测试', '功能测试'],
        ['性能测试', '性能测试'],
        ['接口测试', '接口测试']
    ]

    CASE_STAGE = [
        ['功能测试阶段', '功能测试阶段'],
        ['系统测试阶段', '系统测试阶段'],
        ['冒烟测试阶段', '冒烟测试阶段'],
    ]

    CASE_PRIORITY = [
        [1,1],
        [2,2],
        [3,3],
        [4,4],
    ]

    RESULT = [
        ['unexecuted', 'unexecuted'],  # 未执行
        ['pass', 'pass'],  # 通过
        ['fail', 'fail'],  # 失败
    ]

    modular = models.ForeignKey(ChanDaoModular,on_delete=models.CASCADE,verbose_name="模块")
    title = models.CharField(max_length=30,verbose_name="用例标题")
    preconditions =  models.CharField(max_length=200,verbose_name="前置条件")
    case_type = models.CharField(max_length=10,verbose_name="用例类型",choices=CASE_TYPE,default='功能测试')
    case_stage = models.CharField(max_length=10,verbose_name="适用阶段",choices=CASE_STAGE,default='功能测试阶段')
    case_priority = models.IntegerField(verbose_name="优先级",choices=CASE_PRIORITY)
    remarks = models.CharField(max_length=3000,verbose_name="备注")
    user = models.ForeignKey(users, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    result = models.CharField(max_length=3000,verbose_name="用例结果",choices=RESULT,default='unexecuted')
    create_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    found_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = "fusion_chandao_case"
        verbose_name="阐道_用例"
        verbose_name_plural=verbose_name
    def __str__(self):
        return "{}".format(self.title)

class ChanDaoCaseStep(models.Model):
    """
    测试步骤
    """
    RESULT = [
        ['unexecuted', 'unexecuted'],  # 未执行
        ['pass', 'pass'],  # 通过
        ['fail', 'fail'],  # 失败
        ['block','block'], #阻塞
    ]

    case = models.ForeignKey(ChanDaoCase,on_delete=models.CASCADE,null=True,related_name="case")
    step = models.CharField(max_length=3000,verbose_name="步骤")
    expect = models.CharField(max_length=3000,verbose_name="预期")
    case_result = models.CharField(max_length=3000,verbose_name="用例结果",choices=RESULT,default='unexecuted')
    remarks = models.CharField(max_length=3000,blank=True,null=True,verbose_name="备注")

    class Meta:
        db_table = "fusion_chandao_step"
        verbose_name="阐道_用例步骤"
        verbose_name_plural=verbose_name
    def __str__(self):
        return "{}".format(self.case)

