# -*-coding:utf-8 -*-


import oss2
from linerunner.settings import logger
class UploadOss():
    def oss_file(self,yourObjectName,yourLocalFile):
        # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
        auth = oss2.Auth('LTAI4FiCEjxYhPAnoTTvhUv4', '4vOYTEfnXWrlnmbb9kqKMUKtSS7gEf')
        # Endpoint以杭州为例，其它Region请按实际情况填写。
        bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', 'brc03')

        # <yourObjectName>上传文件到OSS时需要指定包含文件后缀在内的完整路径，例如abc/efg/123.jpg。
        # <yourLocalFile>由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
        logger.info("地址:{}".format(yourObjectName))
        logger.info("oss修改的路径:{}".format(yourObjectName))
        result = bucket.put_object_from_file(yourObjectName, yourLocalFile)
        urls = bucket.sign_url('GET', yourObjectName, 3600 * 1000 * 24 * 365 * 10)
        logger.info("oss返回地址:{}".format(urls))
        #处理url后面的参数
        url =urls.split(yourObjectName)[0]+yourObjectName
        logger.info("oss处理后的url:{}".format(url))
        return url
        # bucket.get_object_to_file()

    def oss_down(self,yourObjectName,yourLocalFile):
        auth = oss2.Auth('LTAI4FiCEjxYhPAnoTTvhUv4', '4vOYTEfnXWrlnmbb9kqKMUKtSS7gEf')
        # Endpoint以杭州为例，其它Region请按实际情况填写。
        bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', 'brc03')

        bucket.get_object_to_file(yourObjectName,yourLocalFile)

# if __name__ == '__main__':
#     import os
#     yourObjectName ="123.xmind"
#     # yourLocalFile="/Users/wuhongbin/Desktop/新版平台/lwjTest/file/123.xmind"
#     # UploadOss().oss_file(yourObjectName,yourLocalFile)
#     # yourObjectName ="http://brc03.oss-cn-hangzhou.aliyuncs.com/%E5%B9%B3%E5%8F%B0%E5%8A%9F%E8%83%BD.xmind?OSSAccessKeyId=LTAI4FiCEjxYhPAnoTTvhUv4&Expires=317017675154&Signature=Tz6f4VB6y%2FXHcvPwKrxi9mAQKY8%3D平台功能.xmind"
#     BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     yourLocalFile = os.path.join(BASE_PATH, 'templates/report')+"/123.xmind"
#     UploadOss().oss_down(yourObjectName,yourLocalFile)
