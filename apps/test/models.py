from django.db import models
from ..user.models import BaseTable
from ..project.models import Modular
from django.conf import settings
from django.contrib.auth import get_user_model

users = get_user_model()


class TestCase(BaseTable):
    """
    测试用例
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
        [1, 1],
        [2, 2],
        [3, 3],
        [4, 4],
    ]

    RESULT = [
        ['unexecuted', 'unexecuted'],  # 未执行
        ['pass', 'pass'],  # 通过
        ['fail', 'fail'],  # 失败
    ]

    modular = models.ForeignKey(Modular, on_delete=models.CASCADE, verbose_name="模块")
    title = models.CharField(max_length=30, verbose_name="用例标题")
    preconditions = models.CharField(max_length=200, verbose_name="前置条件")
    case_type = models.CharField(max_length=10, verbose_name="用例类型", choices=CASE_TYPE, default='功能测试')
    case_stage = models.CharField(max_length=10, verbose_name="适用阶段", choices=CASE_STAGE, default='功能测试阶段')
    case_priority = models.IntegerField(verbose_name="优先级", choices=CASE_PRIORITY)
    remarks = models.CharField(max_length=3000, verbose_name="备注")
    user = models.ForeignKey(users, on_delete=models.SET_NULL, null=True, verbose_name='创建人')
    result = models.CharField(max_length=3000, choices=RESULT, default='unexecuted', verbose_name="用例结果")

    class Meta:
        db_table = "testcase"
        verbose_name = "测试用例"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.title)


class TestCaseStep(BaseTable):
    """
    用例步骤
    """

    RESULT = [
        ['unexecuted', 'unexecuted'],  # 未执行
        ['pass', 'pass'],  # 通过
        ['fail', 'fail'],  # 失败
        ['block', 'block'],  # 阻塞
    ]

    case = models.ForeignKey(TestCase, on_delete=models.CASCADE, null=True, related_name="case")
    step = models.CharField(max_length=3000, verbose_name="步骤")
    expect = models.CharField(max_length=3000, verbose_name="预期")
    case_result = models.CharField(max_length=3000, verbose_name="用例结果", choices=RESULT, default='unexecuted')
    remarks = models.CharField(max_length=3000, blank=True, null=True, verbose_name="备注")

    class Meta:
        db_table = "testcase_step"
        verbose_name = "用例步骤"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.case)


class Bugtracker(BaseTable):
    """
    缺陷跟踪表
    """
    BUG_TYPE_CHOICE = (
        (0, '功能缺陷'),
        (1, 'UI缺陷'),
        (2, '易用性缺陷'),
        (3, '安全缺陷'),
        (4, '性能缺陷'),
    )

    BUG_SERVERITY_CHOICE = (
        (0, 'P0'),
        (1, 'P1'),
        (2, 'P2'),
        (3, 'P3'),
    )

    BUG_STATE_CHOICE = (
        (0, '待处理'),
        (1, '处理中'),
        (2, '待验证'),
        (3, '已解决'),
        (4, '已拒绝'),
        (5, '已挂起'),
        (6, '已关闭'),
    )

    title = models.CharField(max_length=50, verbose_name='Bug')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    attachment = models.CharField(max_length=1024, blank=True, null=True, verbose_name='附件')
    type = models.IntegerField(blank=True, null=True, choices=BUG_TYPE_CHOICE, verbose_name='缺陷类型')
    severity = models.IntegerField(blank=True, null=True, choices=BUG_SERVERITY_CHOICE, verbose_name='严重等级')
    module = models.ForeignKey(Modular, on_delete=models.CASCADE, blank=True, null=True, verbose_name='所属模块')
    handler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                related_name='bugtracker_handler', verbose_name='处理人')
    state = models.IntegerField(choices=BUG_STATE_CHOICE, default=0, verbose_name="状态")

    class Meta:
        db_table = "test"
        verbose_name = "缺陷跟踪"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.title)
