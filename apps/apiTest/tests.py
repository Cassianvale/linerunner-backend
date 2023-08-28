from django.test import TestCase
import os
# Create your tests here.


import requests
from urllib import parse
import json
import re

# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from linerunner.settings import logger
from ast import literal_eval
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

#自定义函数
arguments={"case1":"111"}
a='{"name":"123","name1":"456"}'
b='{"case":"{{case1}}"}'
c='{"case":"___int{5}"}'
d='{"name":"123","name1":{"case":"{{case1}}"}}'
e='{"name":"123","name1":{"case":"___int{5}"}}'
g='{"name":"___int{5}","name1":{"case":"___int{5}"}}'
f=[a,b,c,d,e,g]
for i in f:
    print(data_result_dict(i,arguments))






