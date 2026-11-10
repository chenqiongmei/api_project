import json

import allure
import requests
import urllib3
from common.recordlog import logs
from conf.setting import API_TIMEOUT
from common.operyaml import ReadYamlData
from requests import utils


class SendRequests:

    def __init__(self):
        self.read = ReadYamlData()

    def send_requests(self, **kwargs):
        cookie = {}
        session = requests.session()
        result = session.request(**kwargs)
        set_cookie = requests.utils.dict_from_cookiejar(result.cookies)
        if set_cookie:
            cookie['Cookie'] = set_cookie
            self.read.write_yaml_data(cookie)
            logs.info("cookie：%s" % cookie)
        logs.info("接口返回信息：%s" % result.text if result.text else result)
        return result

    def run_main(self, name, url, case_name, header, method, cookies=None, file=None, **kwargs):
        try:
            # 收集报告日志信息
            logs.info('接口名称：{}'.format(name))
            logs.info('接口请求地址：{}'.format(url))
            logs.info(f'测试用例名称：{case_name}')
            logs.info(f'请求头：{header}')
            logs.info(f'cookies：{cookies}')
            req_params = json.dumps(kwargs, ensure_ascii=False)

            # kwargs = {'data': {'user_name': '${get_params()}', 'passwd': 'admin123'}}
            if 'data' in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info(f'请求参数：{kwargs}')
            elif 'json' in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info(f'请求参数：{kwargs}')
            elif 'params' in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                logs.info(f'请求参数：{kwargs}')
            response = self.send_requests(method=method, url=url, headers=header, cookies=cookies, files=file,
                                          timeout=API_TIMEOUT, verify=False, **kwargs)
            return response
        except Exception as e:
            logs.error(e)

# if __name__ == '__main__':
#     send = SendRequests()
#     url = 'http://127.0.0.1:8787/dar/user/login'
#     data = {'user_name': 'test01', 'passwd': 'admin123'}
#     header = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
#     result = send.send_requests(url=url, data=data, headers=header, method='post')
#     print(result.text)
