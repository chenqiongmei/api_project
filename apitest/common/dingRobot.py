import base64
import hashlib
import hmac
import time
import urllib.parse

import requests


def generate_sign():
    """
    签名计算
    :return:
    """
    timestamp = str(round(time.time() * 1000))
    # 钉钉机器人里面生成的秘钥
    secret = 'SECb163daa45904540212492d8ad7bf7c3ce428fae5211c2e94b1f0926be0778191'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    return timestamp, sign


def send_dingding_msg(content, at_all=True):
    """
    像钉钉群机器人推送结果
    :param content: 发送的内容
    :param at_all: @钉钉群里的全部人，默认为True
    :return:
    """
    timestamp_sign = generate_sign()
    # 首先需要拿到钉钉机器人的webhook地址+timestamp+sign
    url = f'https://oapi.dingtalk.com/robot/send?access_token=df849617e1f9593fd9c31f75ce4fdf2fea8fec39c7b714a65f20413444f5cea5&timestamp={timestamp_sign[0]}&sign={timestamp_sign[1]}'
    headers = {'Content-type': 'application/json;charset=utf-8'}
    req_data = {
        'msgtype': 'text',
        'text': {
            'content': content
        },
        'at': {
            'isAtAll': at_all
        }
    }
    res = requests.post(url=url, json=req_data, headers=headers)
    return res.text
