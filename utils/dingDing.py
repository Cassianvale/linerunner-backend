# -*-coding:utf-8 -*-
import requests,json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from linerunner.settings import DINGDING_URL
class DingDing(object):
    def __init__(self):
        pass

    def get_message(self,content):
            self.url = DINGDING_URL
            self.pagrem = {
                "msgtype": "text",
                "text": {
                    "content": content
                },
                "isAtAll": True
            }
            self.headers = {
                'Content-Type': 'application/json'
            }
            requests.post(url=self.url, data=json.dumps(self.pagrem), headers=self.headers,verify=False)

# if __name__ == '__main__':
#     DingDing().get_message("remarks:测试")
