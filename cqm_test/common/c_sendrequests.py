# -*- coding: utf-8 -*-
import json
import requests
from common.c_recordlog import logs
from requests import utils
from common.c_read_yaml import ReadYamlData
import pytest

class SendRequests(object):
    """
    封装接口请求

    """
    def __init__(self):
        self.read = ReadYamlData()

    def get(self, url, data, header):
        """
        封装get请求
        :param url:请求地址
        :param data:请求参数
        :param header:请求头
        :return:返回值

        """
        if header is None:
            res = requests.get(url=url, params=data)
        else:
            res = requests.get(url=url, params=data, headers=header)
        return res.json()

    def post(self, url, data, header):
        """
        封装post请求
        :param url:请求地址
        :param data:请求参数
        :param header:请求头
        :return:返回值
        """
        if header is None:
            res = requests.post(url, data, verify=False)
        else:
            res = requests.post(url, data, headers=header, verify=False)
        return res.json()

    def put(self):
        pass

    def delete(self):
        pass

    def send_request(self, **kwargs):
        cookie = {}
        session = requests.session()
        result = None
        try:
            result = session.request(**kwargs)
            set_cookie = requests.utils.dict_from_cookiejar(result.cookies)
            if set_cookie:
                cookie['Cookie'] = set_cookie
                self.read.write_yaml_data(set_cookie)
                logs.info(f'cookie: {cookie}')
            logs.info(f'接口的实际返回信息：{result.text if result.text else result}')
        except requests.exceptions.ConnectionError:
            logs.error('接口连接服务器异常！')
            pytest.fail('接口请求异常，可能是request的连接数过多或者请求速度过快导致程序报错！')
        except requests.exceptions.HTTPError:
            logs.error('http异常')
            pytest.fail('http请求异常！')
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail('请求异常，请检查系统或数据是否正常！')
        return result

    def run_main(self, name, url, case_name, header, method, cookies=None, file=None, **kwargs):
    # def run_main(self, url, data, header, method):
    #     res = None
    #             if method.upper() == 'GET':
    #                 res = self.get(url,data,header)
    #             elif method.upper() == 'POST':
    #                 res = self.post(url,data,header)
    #             else:
    #                 print('暂时仅支持get/post请求')
    #             return res
        """
        封装主函数
        :param url:请求地址
        :param data:请求参数
        :param header:请求头
        :param method:请求方法
        :return:返回值
        """
        # 收集报告日志
        try:
            logs.info(f'接口名称:{name}')
            logs.info(f'接口地址:{url}')
            logs.info(f'请求方法:{method}')
            logs.info(f'用例名称:{case_name}')
            logs.info(f'请求头:{header}')
            logs.info(f'cookies:{cookies}')
            req_params = json.dumps(kwargs,ensure_ascii=False)
            if 'data' in kwargs:
                logs.info(f'表单请求参数：{kwargs["data"]}')
            elif 'json' in kwargs:
                logs.info(f'JSON请求参数：{kwargs["json"]}')
            elif 'params' in kwargs:
                logs.info(f'URL查询参数：{kwargs["params"]}')
        except Exception as e:
            logs.exception(e)
            response = self.send_request(method=method, url=url, headers=header, cookies=cookies, files=file, verufy=False, **kwargs)
            return response




if __name__ == '__main__':
    url = "http://127.0.0.1:8787/dar/user/login"
    data = {"user_name": "test01", "passwd": "admin123"}
    method = 'post'
    header = None
    # ---------实例化-----------
    send = SendRequests()
    res = send.run_main(url=url, data=data, header=header, method=method)
    print(res)
