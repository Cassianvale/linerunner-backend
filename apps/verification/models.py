from django.db import models

# class SmsCode(models.Model):
#     TYPE = (
#         ("1","1",), #注册发送验证码
#         ("2","2"),  #修改密码发送验证码
#     )
#     mobile = models.CharField(max_length=11,verbose_name="手机号")
#     type = models.CharField(max_length=2,choices=TYPE,verbose_name="验证码类型")
#     code = models.CharField(max_length=6,verbose_name="验证码")
#     class Meta:
#         db_table="linerunner_sms"
#         verbose_name="验证码"
#         verbose_name_plural = verbose_name
#     def __str__(self):
#         return self.mobile