from django.db import models
from ..user.models import BaseTable
from ..chanDao.models import ChanDaoModular
from django.conf import settings

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

class Bugtracker(BaseTable):
    """
    缺陷跟踪表
    """
    title = models.CharField(max_length=50, verbose_name='Bug')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    attachment = models.CharField(max_length=1024, blank=True, null=True, verbose_name='附件')
    type = models.IntegerField(blank=True, null=True, choices=BUG_TYPE_CHOICE, verbose_name='缺陷类型')
    severity = models.IntegerField(blank=True, null=True, choices=BUG_SERVERITY_CHOICE, verbose_name='严重等级')
    module = models.ForeignKey(ChanDaoModular, on_delete=models.CASCADE, blank=True, null=True, verbose_name='所属模块')
    handler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                               related_name='bugtracker_handler', verbose_name='处理人')
    state = models.IntegerField(choices=BUG_STATE_CHOICE, default=0, verbose_name="状态")

    class Meta:
        db_table = "bugtracker"
        verbose_name = "缺陷跟踪"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.title)

