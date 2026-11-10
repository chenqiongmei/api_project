# -*- coding: utf-8 -*-
import requests
# 提取cook
from requests import utils

def test_login():
    url = "http://127.0.0.1:8787/dar/user/login"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"user_name": "test01", "passwd": "admin123"}  # 当前有效账号

    r = requests.post(url, data=data, headers=headers)
    print("状态码:", r.status_code)
    # 方法1：解析 JSON，避免 Unicode 字符串匹配问题
    res_json = r.json()
    print("响应JSON:", res_json)

    # 方法2：解析 文本类型转码
    # print(r.text.encode().decode("unicode_escape"))

    assert r.status_code == 200
    # 断言业务成功（根据返回，msg_code 200 即成功，或解码后 msg 含“登录成功”）
    assert res_json["msg_code"] == 200
    # 若需断言中文，可显式解码：assert "登录成功" in res_json["msg"]
    # 确保提取到 token（对齐 YAML 的 extract）
    assert res_json["token"] is not None

    # -----------------------------------注意传参时，看请求类型--------------------------------
    # post请求，表单用 :data = ;json用:json =
    # get请求，统一用:param =

    # ② requests.post()
    # ③ requests.put() 修改
    # ④ requests.delete() 删除
    # ⑤ 创建会话保留身份信息-------------------------------------
    session = requests.session()
    res2 = session.request(method="post", url=url,params=data, headers=headers)
    print(res2.json())
    # ⑥ 获取cookie
    result = session.request(method="post",url=url,data=data)
    requests.utils.dict_from_cookiejar(result.cookies)
    print(result.text)

