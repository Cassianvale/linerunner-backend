# -*-coding:utf-8 -*-

import requests
import json
import os
from .models import Case,CaseApiList,Api
from ..apiTest.api_request import apiRequest
from utils import dictor
from ..apiTest.models import ApiArgument,ApiArgumentExtract
from .models import CaseApiRunRecord,CaseRunRecord
from linerunner.settings import logger
from .serializers import CaseRunRecordSerializer
from ruamel import yaml
from ast import literal_eval
from ..report.models import ReportModel
from utils.dingDing import DingDing
def run_case(case_id):
    """
    单个测试用例执行
    :param case_id:
    :return:
    """
    case = Case.objects.get(pk=case_id)
    case_record = CaseRunRecord.objects.create(case=case)
    # 全局参数
    global_arguments = {}
    #运行API以及添加API参数
    case_apis = CaseApiList.objects.filter(case_id=case_id)
    for api in case_apis:
        #全局变量参数写入公共字典
        case_arguments = ApiArgument.objects.filter(api=api.api_id)
        for case_argument in case_arguments:
            global_arguments[case_argument.name] = case_argument.value
        #获取测试用例里的api，是否需要重置请求参数
        reset_data = CaseApiList.objects.filter(case_id=case_id,api=api.api_id)[0].reset_data
        # 运行api
        if reset_data=='':
            api_model = Api.objects.get(id=api.api_id)
            resp = apiRequest(api=api_model, arguments=global_arguments)[0]
        else:
            api_model = Api.objects.get(id=api.api_id)
            resp = apiRequest(api=api_model, arguments=global_arguments,reset_data=reset_data)[0]

        #保存case的api运行记录
        CaseApiRunRecord.objects.create(
            name=api_model.name,
            url=resp.url,
            http_method=resp.request.method,
            data=resp.request.body,
            headers=resp.request.headers,
            return_code=resp.status_code,
            return_content=resp.text,
            return_time=resp.elapsed.total_seconds(),
            api=api_model,
            case_record=case_record
        )
        #运行API后，看下是否还有参数需要提取
        api_arguments = ApiArgumentExtract.objects.filter(api_id=api_model.id)
        if api_arguments:
            for api_argument in api_arguments:
                dictor_data = {}
                # 请求头
                if api_argument.origin == 'HEADER':
                    dictor_data = resp.headers
                    logger.info("headers—response:{}".format(dictor_data))
                elif api_argument.origin == 'COOKIE':
                    # 获取cookies返回的字典
                    dictor_data = requests.utils.dict_from_cookiejar(resp.cookies)
                    logger.info("cookies-response:{}".format(dictor_data))
                    # 响应
                elif api_argument.origin == 'BODY':
                    dictor_data = resp.json()
                    logger.info("body-response:{}".format(dictor_data))
                argument_value = dictor.dictor(dictor_data, api_argument.format)
                global_arguments[api_argument.name] = argument_value
                logger.info(global_arguments)
    logger.info("全局参数:{}".format(global_arguments))
    serializer = CaseRunRecordSerializer(case_record).data
    result_json = json.dumps(serializer, ensure_ascii=False)
    result_dict = json.loads(result_json)
    logger.info("result_dict:{}".format(result_dict))
    response_data = result_dict.get("api_records")
    api_response_list = []
    for i in range(len(response_data)):
        # 用例名称
        case_name_dict = result_dict.get("case")
        case_name = case_name_dict.get("name")
        # api名称
        name_dict = response_data[i].get("api")
        name = name_dict.get("name")
        # 预期状态码
        expect_code_dict = response_data[i].get("api")
        expect_code = int(expect_code_dict.get("expect_code"))
        # 预期结果
        expect_content_dict = response_data[i].get("api")
        expect_content = expect_content_dict.get("expect_content")
        # 请求url
        url = response_data[i].get("url")
        # 请求方法
        method = response_data[i].get("http_method")
        # 参数
        data = response_data[i].get("data")
        # 响应状态码
        return_code = int(response_data[i].get("return_code"))
        # 响应内容
        return_content = response_data[i].get("return_content")
        #断言内容
        #判断是否已重置断言内容
        api_id = response_data[i]['api'].get("id")
        # try:
        reset_expect_content = CaseApiList.objects.get(case_id=case_id,index=i,api_id=api_id).reset_expect_content
        if reset_expect_content=='':
            assert_content = response_data[i]['api'].get("expect_content")
        else:
            assert_content = reset_expect_content

        reset_expect_content = CaseApiList.objects.get(case_id=case_id,index=i,api_id=api_id).reset_expect_code
        if reset_expect_content=='':
            expect_code = expect_code
        else:
            expect_code = int(reset_expect_content)


        #断言状态码
        remarks = []
        if expect_code == return_code:
            # 断言内容
            logger.info("断言数据:{}".format(response_data[i].get("expect_content")))
            if expect_content:
                # 遍历断言内容
                for assert_content in literal_eval(expect_content):
                    for key,value in assert_content.items():
                        actual_value = key
                        assert_value = dictor.dictor(json.loads(return_content), value)
                        # 每个内容断言确认
                        if type(assert_value)==int:
                            if int(actual_value) == assert_value:
                                assert_code = "pass"
                            else:
                                assert_code = "fail"
                                remarks.append(
                                    "断言内容不一致，响应数据提取内容:{},预期内容:{},实际内容:{}".format(assert_content, assert_value,
                                                                                 actual_value))
                                logger.error("断言内容不一致，预期内容:{},实际内容:{}".format(assert_value, actual_value))
                                break
                        elif type(assert_value)==float:
                            if float(actual_value) == assert_value:
                                assert_code = "pass"
                            else:
                                assert_code = "fail"
                                remarks.append(
                                    "断言内容不一致，响应数据提取内容:{},预期内容:{},实际内容:{}".format(assert_content, assert_value,
                                                                                 actual_value))
                                logger.error("断言内容不一致，预期内容:{},实际内容:{}".format(assert_value, actual_value))
                                break
                        elif type(assert_value)==str:
                            if actual_value == assert_value:
                                assert_code = "pass"
                            else:
                                assert_code = "fail"
                                remarks.append(
                                    "断言内容不一致，响应数据提取内容:{},预期内容:{},实际内容:{}".format(assert_content, assert_value,
                                                                                 actual_value))
                                logger.error("断言内容不一致，预期内容:{},实际内容:{}".format(assert_value, actual_value))
                                break
            else:
                assert_code = "pass"
        # 状态码不一致
        else:
            assert_code = "fail"
            remarks.append("状态码不一致，预期状态码:{},实际状态码:{}".format(expect_code, return_code))
            logger.error("状态码不一致，预期状态码:{},实际状态码:{}".format(expect_code, return_code))
    # except Exception as e:
    #     logger.error("断言报错:{}".format(e))
    #     assert_code = "fail"
        if assert_code == "fail":
            content = "url:{}\n" \
                      "method:{}\n" \
                      "data:{}\n" \
                      "expect_code:{}\n" \
                      "expect_content:{}\n" \
                      "return_code:{}\n" \
                      "assert_code:{}\n" \
                      "return_content:{}\n" \
                      "remarks:{}".format(url, method, data, expect_code, expect_content, return_code, assert_code,
                                          return_content, remarks)
            DingDing().get_message(content)

        api_response_list.insert(i, [case_name, name, url, method, data, return_code, expect_code, return_content,assert_code])
    with open("utils/response.txt", "w") as f:
        f.write(json.dumps(api_response_list, ensure_ascii=False))
    os.system('python3 utils/testSingleSuite.py')
    curpath = os.path.dirname(os.path.realpath(__file__))  # 获取文件当前路径
    yamlpath = os.path.join(curpath, "../../utils/case.yaml")  # 获取yaml文件地址
    data = open(yamlpath, 'r')
    report_data = yaml.load(data.read(), Loader=yaml.Loader)
    ReportModel.objects.create(
        project_name=report_data['project_name'],
        project_host=report_data['project_host'],
        case_type=report_data['case_type'],
        case_all=report_data['case_all'],
        case_pass=report_data['case_pass'],
        case_fail=report_data['case_fail'],
        start_time=report_data['start_time'],
        run_time=report_data['run_time'],
        report_details=report_data['report_details']
    )
    return case_record

def run_case_list(case_id_list):
    """
    批量执行测试用例
    :param case_id_list:
    :return:
    """
    case_response_list = []
    for case_id in list(case_id_list):
        serializer_list = []
        # 全局参数
        global_arguments = {}
        case = Case.objects.get(pk=case_id)
        case_record = CaseRunRecord.objects.create(case=case)

        case_apis = CaseApiList.objects.filter(case_id=case_id)
        for api in case_apis:
            # 请求参数重置
            reset_data = api.reset_data
            case_arguments = ApiArgument.objects.filter(api=api.api_id)
            # 获取api下的全局参数替换
            for case_argument in case_arguments:
                global_arguments[case_argument.name] = case_argument.value
            # 运行api
            # 获取测试用例里的api，是否需要重置请求参数
            reset_data = CaseApiList.objects.filter(case_id=case_id, api=api.api_id)[0].reset_data
            # 运行api
            if reset_data == '':
                api_model = Api.objects.get(id=api.api_id)
                resp = apiRequest(api=api_model, arguments=global_arguments)[0]
            else:
                api_model = Api.objects.get(id=api.api_id)
                resp = apiRequest(api=api_model, arguments=global_arguments, reset_data=reset_data)[0]
        #     # 运行API以及添加API参数
        # api_model_list = case.api_list.all()
        # # 遍历测试用例的api
        # for api_model in api_model_list:
        #     case_arguments = ApiArgument.objects.filter(api=api_model.id)
        #     # 获取api下的全局参数替换
        #     for case_argument in case_arguments:
        #         global_arguments[case_argument.name] = case_argument.value
            # 运行api
            # resp = linerunnerrequest.linerunnerrequest(api_model, global_arguments)
            # 保存case下的api的运行记录
            CaseApiRunRecord.objects.create(
                name=api_model.name,
                url=resp.url,
                http_method=resp.request.method,
                data=resp.request.body,
                headers=resp.request.headers,
                return_code=resp.status_code,
                return_content=resp.text,
                return_time=resp.elapsed.total_seconds(),
                api=api_model,
                case_record=case_record
            )
            logger.info("{}：运行记录保存成功".format(api_model.name))
            #         # 运行API后，看下是否还有参数需要提取
            api_arguments = ApiArgumentExtract.objects.filter(api_id=api_model.id)
            if api_arguments:
                for api_argument in api_arguments:
                    dictor_data = {}
                    # 请求头
                    if api_argument.origin == 'HEAD':
                        dictor_data = resp.headers
                        logger.info("headers—response:{}".format(dictor_data))
                    elif api_argument.origin == 'COOKIE':
                        # 获取cookies返回的字典
                        dictor_data = requests.utils.dict_from_cookiejar(resp.cookies)
                        logger.info("cookies-response:{}".format(dictor_data))
                        # 响应
                    elif api_argument.origin == 'BODY':
                        dictor_data = resp.json()
                        logger.info("body-response:{}".format(dictor_data))
                    argument_value = dictor.dictor(dictor_data, api_argument.format)
                    global_arguments[api_argument.name] = argument_value
                    logger.info(global_arguments)
        logger.info("全局参数:{}".format(global_arguments))
        serializer = CaseRunRecordSerializer(case_record).data
        serializer_list.append(serializer)
        result_json = json.dumps(serializer, ensure_ascii=False)
        result_dict = json.loads(result_json)
        logger.info(result_dict)
        # 从反序列化获取数据
        response_data = result_dict.get("api_records")
        api_response_list = []
        for i in range(len(response_data)):
            # 用例名称
            case_name_dict = result_dict.get("case")
            case_name = case_name_dict.get("name")
            # api名称
            name_dict = response_data[i].get("api")
            name = name_dict.get("name")
            # 预期状态码
            expect_code_dict = response_data[i].get("api")
            expect_code = int(expect_code_dict.get("expect_code"))
            # 预期结果
            expect_content_dict = response_data[i].get("api")
            expect_content = expect_content_dict.get("expect_content")
            # 请求url
            url = response_data[i].get("url")
            # 请求方法
            method = response_data[i].get("http_method")
            # 参数
            data = response_data[i].get("data")
            # 响应状态码
            return_code = int(response_data[i].get("return_code"))
            # 响应内容
            return_content = response_data[i].get("return_content")
            # 断言内容
            # 判断是否已重置断言内容
            api_id = response_data[i]['api'].get("id")
            try:
                reset_expect_content = CaseApiList.objects.get(case_id=case_id, index=i,
                                                               api_id=api_id).reset_expect_content
                if reset_expect_content == '':
                    assert_content = response_data[i]['api'].get("expect_content")
                else:
                    assert_content = reset_expect_content

                reset_expect_content = CaseApiList.objects.get(case_id=case_id, index=i,
                                                               api_id=api_id).reset_expect_code
                if reset_expect_content == '':
                    expect_code = expect_code
                else:
                    expect_code = int(reset_expect_content)

                # 断言状态码
                remarks = []
                if expect_code == return_code:
                    # 断言内容
                    logger.info("断言数据:{}".format(response_data[i].get("expect_content")))
                    if expect_content:
                        # 遍历断言内容
                        for assert_content in literal_eval(expect_content):
                            for key, value in assert_content.items():
                                actual_value = key
                                assert_value = dictor.dictor(json.loads(return_content), value)
                                # 每个内容断言确认
                                if actual_value == assert_value:
                                    assert_code = "pass"
                                else:
                                    assert_code = "fail"
                                    remarks.append(
                                        "断言内容不一致，响应数据提取内容:{},预期内容:{},实际内容:{}".format(assert_content, assert_value,
                                                                                     actual_value))
                                    logger.error("断言内容不一致，预期内容:{},实际内容:{}".format(assert_value, actual_value))
                                    break
                    else:
                        assert_code = "pass"
                # 状态码不一致
                else:
                    assert_code = "fail"
            except Exception as e:
                logger.error("断言报错:{}".format(e))
                assert_code = "fail"
            api_response_list.insert(i, [case_name, name, url, method, data, return_code, expect_code, return_content,
                                         assert_code])
        case_response_list.append(api_response_list)
    with open("utils/response.txt", "w") as f:
        f.write(json.dumps(case_response_list, ensure_ascii=False))
    os.system('python3 utils/testManySuite.py')
    curpath = os.path.dirname(os.path.realpath(__file__))  # 获取文件当前路径
    yamlpath = os.path.join(curpath, "../../utils/case.yaml")  # 获取yaml文件地址
    data = open(yamlpath, 'r')
    report_data = yaml.load(data.read(), Loader=yaml.Loader)
    ReportModel.objects.create(
        project_name=report_data['project_name'],
        project_host=report_data['project_host'],
        case_type=report_data['case_type'],
        case_all=report_data['case_all'],
        case_pass=report_data['case_pass'],
        case_fail=report_data['case_fail'],
        start_time=report_data['start_time'],
        run_time=report_data['run_time'],
        report_details=report_data['report_details']
    )
    return case_response_list


def run_case_test(case_id):
    """
    定时任务调运行用例
    :param case_id:
    :return:
    """
    case_list = literal_eval(case_id)
    #小于2走单个用例的执行
    if len(case_list)<2:
        run_case(case_list[0])
    #走多个用例执行
    else:
        run_case_list(case_list)

