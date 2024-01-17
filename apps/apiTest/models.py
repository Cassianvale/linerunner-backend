from django.db import models
from django.contrib.auth import get_user_model
from ..user.models import BaseTable

# 返回在此项目中处于活动状态的用户模型
users = get_user_model()


# 请求类型
HTTP_METHOD_CHOICE = (
    ('POST', 'POST'),
    ('GET', 'GET'),
    ('PUT', 'PUT'),
    ('DELETE', 'DELETE')
)
# 数据类型
REQUEST_TYPE = (
    ('json', 'json'),
    ('data', 'data')
)


class Project(models.Model):
    """
    项目表
    """
    PROJECTTYPE = [
        ['web', 'web'],
        ['app', 'app']
    ]
    name = models.CharField(max_length=50, verbose_name='项目名称')
    type = models.CharField(max_length=50, verbose_name='项目类型', choices=PROJECTTYPE)
    # blank为存之前判断, null为存之后判断  提交可为空, 数据库可为空
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    create_user = models.ForeignKey(users, on_delete=models.SET_NULL, null=True, verbose_name='创建人')

    class Meta:
        db_table = 'project'
        verbose_name = "项目表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.name)


class Host(models.Model):
    """
    host域名
    """
    name = models.CharField(max_length=50, verbose_name='名称')
    host = models.CharField(max_length=1024, verbose_name='Host地址')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目', related_name='host_list')

    class Meta:
        db_table = "host"
        verbose_name = "host域名"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.host)


class Api(models.Model):
    """
    接口信息
    """
    STATUS_CODE_CHOICE = (
        ('200', '200'),
        ('201', '201'),
        ('202', '202'),
        ('203', '203'),
        ('204', '204'),
        ('301', '301'),
        ('302', '302'),
        ('400', '400'),
        ('401', '401'),
        ('403', '403'),
        ('404', '404'),
        ('405', '405'),
        ('406', '406'),
        ('407', '407'),
        ('408', '408'),
        ('500', '500'),
        ('502', '502')
    )
    name = models.CharField(max_length=50, verbose_name='接口名称')
    http_method = models.CharField(max_length=50, verbose_name='请求方式', choices=HTTP_METHOD_CHOICE)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='host', related_name='host_api', null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目', related_name='api_list',
                                null=True)
    path = models.CharField(max_length=1024, verbose_name='接口地址')
    headers = models.TextField(null=True, blank=True, verbose_name='请求头')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE, verbose_name='请求类型', default='form-data')
    data = models.TextField(null=True, blank=True, verbose_name='提交的数据')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    expect_code = models.CharField(default=200, max_length=10, verbose_name='期望返回的code',
                                   choices=STATUS_CODE_CHOICE)
    expect_content = models.CharField(null=True, max_length=200, verbose_name='期望返回的内容', blank=True)

    class Meta:
        db_table = "api"
        verbose_name = "接口信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.name)


class ApiArgument(models.Model):
    """
    api的全局参数
    """
    api = models.ForeignKey(Api, on_delete=models.CASCADE, verbose_name='用例', null=True, related_name='arguments')
    name = models.CharField(max_length=100, null=True, verbose_name='参数名字')
    value = models.CharField(max_length=100, null=True, verbose_name='参数的值')

    class Meta:
        db_table = "api_argument"
        verbose_name = "api的参数"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.api)


class ApiArgumentExtract(models.Model):
    """
    用例API的响应参数提取
    """
    ARGUMENT_ORIGIN_CHOICE = (
        ('HEADER', 'HEADER'),  # headers提取
        ('BODY', 'BODY'),  # 响应内容提取
        ('COOKIE', 'COOKIE')  # cookie提取
    )
    api = models.ForeignKey(Api, on_delete=models.CASCADE, verbose_name='用例API', null=True,
                            related_name='argumentExtract')
    name = models.CharField(max_length=100, null=True, verbose_name='参数名字')
    origin = models.CharField(max_length=20, null=True, choices=ARGUMENT_ORIGIN_CHOICE, verbose_name='参数来源')
    format = models.CharField(max_length=100, null=True, verbose_name='参数获取的格式')

    class Meta:
        db_table = "api_argument_extract"
        verbose_name = "用例API的参数提取"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.api)


class RunApiRecord(models.Model):
    """
    API运行记录
    """
    name = models.CharField(max_length=200, verbose_name='api名称', null=True)
    url = models.CharField(max_length=200, verbose_name='请求的url')
    http_method = models.CharField(max_length=10, verbose_name='请求方式', choices=HTTP_METHOD_CHOICE)
    data = models.TextField(null=True, verbose_name='提交的数据')
    headers = models.TextField(null=True, verbose_name='提交的header')
    create_time = models.DateTimeField(auto_now=True, verbose_name='运行的时间')
    return_code = models.CharField(max_length=10, verbose_name='返回的code')
    return_content = models.TextField(null=True, verbose_name='返回的内容')
    return_cookies = models.TextField(null=True, verbose_name='返回的cookies')
    return_headers = models.TextField(null=True, verbose_name='返回的headers')
    api = models.ForeignKey(Api, on_delete=models.CASCADE, verbose_name='关联的API', null=True)
    assert_result = models.CharField(max_length=10, null=True, verbose_name='断言结果')

    class Meta:
        ordering = ['-create_time']
        db_table = "run_api_record"
        verbose_name = "api运行记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.url)


class Parameterization(models.Model):
    name = models.CharField(max_length=256, verbose_name='参数化名称', null=True)
    expression = models.CharField(max_length=256, verbose_name='表达式', null=True)
    example = models.CharField(max_length=256, verbose_name='示例', null=True)

    class Meta:
        db_table = "parameterization"
        verbose_name = "参数化表达式"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.name)
