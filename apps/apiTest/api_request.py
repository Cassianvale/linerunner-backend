# -*-coding:utf-8 -*-
import os
import requests
import json
import re
from urllib.parse import urljoin
# from ast import literal_eval
import ast

from linerunner.settings import logger
from utils.dingDing import DingDing
import urllib3
from utils.data_function import DataFunction

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 正则表达式
PATTERN = re.compile(r"{{(.+?)}}")


def _replace_argument(target_str, arguments):
    if isinstance(target_str, (int, bool, float)) or not arguments:
        return target_str

    is_str = isinstance(target_str, str)
    if not is_str:  # 如果目标不是字符串，将其转换为字符串
        target_str = json.dumps(target_str)

    while True:
        match = PATTERN.search(target_str)
        if not match:
            break
        argument_name = match.group(1)
        replace_value = str(arguments[argument_name]) if argument_name in arguments else argument_name
        target_str = PATTERN.sub(replace_value, target_str, count=1)

    return target_str if is_str else json.loads(target_str)  # 如果原始输入是字符串，返回字符串，否则返回字典/列表


# 将正则表达式对象定义在函数外部，避免在每次调用函数时都重新编译
FUNC_EXPR = re.compile(r'___(.*?){(.*?)}')


def data_function(data):
    """接受一个字典作为输入，如果值是字符串并且包含 "___"，则被视为包含自定义函数的字符串"""
    def process_value(value):
        """处理单个值，如果值包含自定义函数，将其替换为处理后的结果"""
        if isinstance(value, str) and "___" in value:
            value_1, value_2 = value.split("___", 1)
            value_2 = "___" + value_2
            funcs = FUNC_EXPR.findall(value_2)
            value = DataFunction().data_parameterization(funcs)
            return str(value_1) + str(value)
        return value

    def recursive_process(data):
        """递归处理字典或列表中的每一个值"""
        if isinstance(data, dict):
            return {k: recursive_process(process_value(v)) for k, v in data.items()}
        elif isinstance(data, list):
            return [recursive_process(process_value(v)) for v in data]
        return data

    return recursive_process(data)


def data_argument(data, arguments):
    data_result = {}
    for key, value in data.items():
        # value使用了自定义函数
        if type(value) == str:
            if "{{" in value:
                data_result[key] = _replace_argument(value, arguments)
            else:
                data_result[key] = value
        elif type(value) == dict:
            data_value = {}
            for k, v in value.items():
                # value使用了自定义函数
                if "{{" in v:
                    data_value[k] = _replace_argument(v, arguments)
                else:
                    data_value[k] = v
            data_result[key] = data_value
    return data_result


def data_result_list(data):
    return data


def data_result_dict(data, arguments):
    data_result = json.loads(data, encoding='utf-8')
    if "___" in data:
        data_result = data_function(data_result)
    if "{{" in data:
        data_result = data_argument(data_result, arguments)
    return data_result


def apiRequest(api, arguments=None):
    host = api.host.host
    method = api.http_method
    request_type = api.request_type
    path = api.path
    url = urljoin(host, path)
    url = _replace_argument(url, arguments)

    # 替换请求参数的变量
    data = dict()

    if api.data:
        # data请求类型的参数格式
        if request_type == "data" or "params":
            request_data_list = literal_eval(api.data)
            logger.info(request_data_list)
            for data_dict in request_data_list:
                for key, value in data_dict.items():
                    if type(value) == str:
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
        # json请求类型的参数格式
        elif request_type == "json":
            data_list = json.loads(api.data, encoding='utf-8')
            if type(data_list) == list:
                data = data_list
            elif type(data_list) == dict:
                if "___" in data:
                    data_result = data_function(data_list)
                if "{{" in data:
                    data_result = data_argument(data_list, arguments)
                data = data_result

    logger.info("请求参数:{}".format(data))
    headers = {}
    if api.headers:
        header_list = json.loads(api.headers, encoding='utf-8')
        for header_dict in header_list:
            for key, value in header_dict.items():
                headers[key] = _replace_argument(value, arguments)

    logger.info(f"请求的url: {url}, 请求参数: {data}, 请求头: {headers}")
    logger.info("==============发起请求====================")

    res = requests.request(method, url, headers=headers, json=data if request_type == "json" else None,
                           data=data if request_type in ["data", "params"] else None, verify=False,
                           allow_redirects=False)
    logger.info(f"response: {res.text}")
    logger.info("==============请求结束====================")

    # 接口响应时间
    runTime = res.elapsed.total_seconds()
    if runTime > 20:
        content = "title:*******响应超时提醒********\n" \
                  "url:{}\n" \
                  "runTime:{}\n".format(url, runTime)
        # DingDing().get_message(content)
    # 保存运行记录
    return res, data
