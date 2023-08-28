# -*-coding:utf-8 -*-

import os
import requests
from urllib import parse
import json
import re
from linerunner.settings import logger
from ast import literal_eval
from utils.dingDing import DingDing
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from utils.data_function import DataFunction


def _replace_argument(target_str,arguments):
    """
    :param target_str: 原始数据
    :param arguments: 需要替换的数据
    :return:
    """
    if type(target_str)==str:
        if not arguments:
            return target_str
        while True:
            search_result = re.search(r"{{(.+?)}}",target_str)
            if not search_result:
                break
            argument_name = search_result.group(1)
            if argument_name in arguments:
                target_str = re.sub("{{"+argument_name+"}}",str(arguments[argument_name]),target_str)
            else:
                target_str = re.sub("{{"+argument_name+"}}",argument_name,target_str)
        return target_str
    elif type(target_str)==dict:
        target_str = json.dumps(target_str)
        if not arguments:
            return target_str
        while True:
            search_result = re.search(r"{{(.+?)}}",target_str)
            if not search_result:
                break
            argument_name = search_result.group(1)
            if argument_name in arguments:
                target_str = re.sub("{{"+argument_name+"}}",arguments[argument_name],target_str)
            else:
                target_str = re.sub("{{"+argument_name+"}}",argument_name,target_str)
        return json.loads(target_str)
    elif type(target_str)==list:
        target_str = str(target_str)
        if not arguments:
            return target_str
        while True:
            search_result = re.search(r"{{(.+?)}}", target_str)
            if not search_result:
                break
            argument_name = search_result.group(1)
            if argument_name in arguments:
                target_str = re.sub("{{" + argument_name + "}}", arguments[argument_name], target_str)
            else:
                target_str = re.sub("{{" + argument_name + "}}", argument_name, target_str)
        return literal_eval(target_str)
    elif type(target_str)==int:
        return target_str
    elif type(target_str)==bool:
        return target_str
    elif type(target_str)==float:
        return target_str

def data_function(data):
    for key,value in data.items():
        #value使用了自定义函数
        if type(value) == str and "___" in value:
            FUNC_EXPR = '___(.*?){(.*?)}'
            value_1 = value.split("___")[0]
            value_2 = "___" + value.split("___")[1]
            funcs = re.findall(FUNC_EXPR, value_2)
            value = DataFunction().data_parameterization(funcs)
            value = str(value_1) + str(value)
            data[key] = value
        elif type(value) == dict:
            data_value={}
            for k, v in value.items():
                # value使用了自定义函数
                if "___" in v:
                    FUNC_EXPR = '___(.*?){(.*?)}'
                    value_1 = v.split("___")[0]
                    value_2 = "___" + v.split("___")[1]
                    funcs = re.findall(FUNC_EXPR, value_2)
                    value = DataFunction().data_parameterization(funcs)
                    value3 = str(value_1) + str(value)
                    data_value[k] = value3
                else:
                    data_value[k]=v
            data[key]=data_value
    return data

def data_argument(data,arguments):
    data_result = {}
    for key,value in data.items():
        #value使用了自定义函数
        if type(value) == str:
            if "{{" in value:
                data_result[key] = _replace_argument(value, arguments)
            else:
                data_result[key] =value
        elif type(value) == dict:
            data_value={}
            for k, v in value.items():
                # value使用了自定义函数
                if "{{" in v:
                    data_value[k] = _replace_argument(v, arguments)
                else:
                    data_value[k]=v
            data_result[key]=data_value
    return data_result


def data_result_list(data):
    return data

def data_result_dict(data,arguments):
    data_result = json.loads(data, encoding='utf-8')
    if "___" in data:
        data_result = data_function(data_result)
    if "{{" in data:
        data_result = data_argument(data_result,arguments)
    return data_result

def apiRequest(api,arguments=None,reset_data=None):
    host = api.host.host
    method = api.http_method
    request_type = api.request_type
    path = api.path
    url = parse.urljoin(host, path)
    url = _replace_argument(url,arguments)
    logger.info("请求的url:{}".format(url))
    #替换请求参数的变量
    data = dict()

    if api.data:
        #data请求类型的参数格式
        if request_type == "data" or "params":
            request_data_list = literal_eval(api.data)
            logger.info(request_data_list)
            for data_dict in request_data_list:
                for key, value in data_dict.items():
                    if type(value) ==str:
                        if "___" in value:
                            FUNC_EXPR = '___(.*?){(.*?)}'
                            funcs = re.findall(FUNC_EXPR, value)
                            original_data = DataFunction().data_parameterization(funcs)
                            data_value = _replace_argument(original_data, arguments)
                            data[key] = data_value
                        else:
                            data_value = _replace_argument(value, arguments)
                            data[key] = data_value
                    else:
                        data[key] = data[value]
        #json请求类型的参数格式
        elif request_type == "json":
                    data_list = json.loads(api.data, encoding='utf-8')
                    if type(data_list)==list:
                        data = data_list
                    elif type(data_list)==dict:
                        if "___" in data:
                            data_result = data_function(data_list)
                        if "{{" in data:
                            data_result = data_argument(data_list, arguments)
                        data =  data_result

                        # for key,value in data_list.items():
                        #     # data[key] = _replace_argument(value,arguments)
                        #     #处理参数需要使用自定义方法
                        #     if type(value)==str and "___" in value:
                        #         FUNC_EXPR = '___(.*?){(.*?)}'
                        #         value_1 = value.split("___")[0]
                        #         value_2 = "___" + value.split("___")[1]
                        #         funcs = re.findall(FUNC_EXPR, value_2)
                        #         value = DataFunction().data_parameterization(funcs)
                        #         value = str(value_1) + str(value)
                        #     #处理参数变量
                        #     if "{{" not in api.data:
                        #         data[key] = value
                        #     else:
                        #         data[key] = _replace_argument(value,arguments)
    logger.info("请求参数:{}".format(data))
    headers = {}
    if api.headers:
        header_list = json.loads(api.headers, encoding='utf-8')
        for header_dict in header_list:
            for key,value in header_dict.items():
                headers[key] = _replace_argument(value,arguments)
    logger.info("请求头:{}".format(headers))
    logger.info("==============发起请求====================")
    if request_type=="json":
        res = requests.request(method, url, headers=headers, json=data,verify=False,allow_redirects=False)
        logger.info("response:{}".format(res.text))
    elif request_type == "data":
        res = requests.request(method, url, headers=headers, data=data, verify=False, allow_redirects=False)
        logger.info("response:{}".format(res.text))
    elif request_type=="params":
        res = requests.request(method, url, headers=headers, params=data,verify=False,allow_redirects=False)
        logger.info("response:{}".format(res.text))
    logger.info("==============请求结束====================")
    #接口响应时间
    runTime = res.elapsed.total_seconds()
    if runTime>20:
        content="title:*******响应超时提醒********\n" \
                "url:{}\n" \
                "runTime:{}\n".format(url,runTime)
        # DingDing().get_message(content)
    # 保存运行记录
    return res,data

