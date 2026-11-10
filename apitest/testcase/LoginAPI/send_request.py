# -*- coding: utf-8 -*-
import requests
class SendRequests(object):
    """
    封装接口请求

    """

    def __init__(self):
        pass

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

    def run_main(self,url, data, header,method):
        """
        封装主函数
        :param url:请求地址
        :param data:请求参数
        :param header:请求头
        :param method:请求方法
        :return:返回值
        """
        res = None
        if method.upper() == 'GET':
            res = self.get(url,data,header)
        elif method.upper() == 'POST':
            res = self.post(url,data,header)
        else:
            print('暂时仅支持get/post请求')
        return res



if __name__ == '__main__':
    url = "http://127.0.0.1:8787/dar/user/login"
    data = {"user_name": "test01", "passwd": "admin123"}
    method = 'post'
    header = None
    # ---------实例化-----------
    send = SendRequests()
    res = send.run_main(url=url, data=data, header=header, method=method)
    print(res)
