from django.shortcuts import render
import random
from . import config
from lwjTest.settings import *
from rest_framework.views import APIView
from django_redis import get_redis_connection
from utils.apiResponse import ApiResponse
from rest_framework import status
from celery_tasks.sms.tasks import send_sms_code
from celery_tasks.sms.yuntongxun.sms import CCP
class SmsCodeAPIView(APIView):
    """
    发送验证码
    """
    def post(self, request, mobile):
        """
        :param request:
        :param mobile: 手机号
        # :param type: 验证码类型
        :return:
        """
        #redis连接
        redis_conn = get_redis_connection("verify_code")
        send_mobile = redis_conn.get("send_{}".format(mobile))
        #判断是否已经发送验证码
        if send_mobile:
            return ApiResponse(http_status=status.HTTP_400_BAD_REQUEST,msg="手机号频繁发送",status=1)
        #生成验证码
        sms_code = "%06d"%random.randint(0,999999)
        logger.info("验证码:{}".format(sms_code))
        #创建redis管道
        pl = redis_conn.pipeline()
        #开启事务
        pl.multi()
        #添加命令到管道
        #验证码
        pl.setex("sms_{}".format(mobile), config.SEND_SMS_CODE_INTERVAL, sms_code)
        #标记
        pl.setex('send_%s' % mobile, config.SEND_SMS_CODE_INTERVAL, 1)
        #执行管道中的命令
        pl.execute()
        #send_sms_code需要2个参数(手机号和验证码)
        send_sms_code.delay(mobile, sms_code)
        return ApiResponse(results="验证码发送成功")

