import time
import urllib.parse
# 注：截图中未显示以下两个导入，但生成签名逻辑中使用了，需补充
import hmac
import hashlib
import base64
import requests


def generate_sign():
    """
    签名计算（钉钉机器人加签安全设置）
    :return: timestamp（时间戳）, sign（签名）
    """
    # 获取当前毫秒级时间戳
    timestamp = str(round(time.time() * 1000))

    # 钉钉机器人里面生成的秘钥（加签模式下的 Secret）
    secret = 'SECb163daa45904540212492d8ad7bf7c3ce428fae5211c2e94b1f0926be0778191'

    # 将秘钥编码为 utf-8 字节
    secret_enc = secret.encode('utf-8')

    # 拼接字符串：时间戳 + '\n' + 秘钥
    string_to_sign = '{}\n{}'.format(timestamp, secret)

    # 将待签名字符串编码为 utf-8 字节
    string_to_sign_enc = string_to_sign.encode('utf-8')

    # HMAC-SHA256 加密计算
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()

    # Base64 编码后进行 URL 编码（quote_plus 处理特殊字符），得到最终签名
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    return timestamp, sign


def send_dingding_msg(content, at_all=True):
    """
    向钉钉群机器人推送结果
    :param content: 发送的内容（文本）
    :param at_all: @钉钉群里的全部人，默认为True
    :return: 接口返回结果（截图中下方请求逻辑被截断，此处保留现有结构）
    """
    # 1. 获取签名和时间戳
    timestamp_sign = generate_sign()

    # 2.拼接最终请求地址：webhook地址 + timestamp + sign
    # access_token 为机器人唯一标识（截图中右侧被截断，此处按可见部分还原）
    url = f'https://oapi.dingtalk.com/robot/send?access_token=df849617e1f9593fd9c31f75ce4fdf2fea8fec39c7b714a65f20413444f5cea5&timestamp={timestamp_sign[0]}&sign={timestamp_sign[1]}'

    # 3. 构造请求头（注：截图原代码为 Content-type，标准写法通常为 Content-Type）
    headers = {'Content-Type': 'application/json;charset=utf-8'}

    # 4. 构造钉钉机器人要求的 JSON 请求体
    req_data = {
        'msgtype': 'text',  # 消息类型为文本
        'text': {
            'content': content  # 发送的具体文本内容
        },
        'at': {
            'isAtAll': at_all  # 是否 @所有人
        }
    }

    # 5. 发送 POST 请求（使用 json 参数自动序列化并携带 Content-Type）
    res = requests.post(url=url, json=req_data, headers=headers)
    # 6. 返回响应文本
    return res.text


if __name__ == '__main__':
    # 脚本直接运行测试：发送测试内容并打印接口返回
    # print(send_dingding_msg(''))
    print(send_dingding_msg('接口自动化测试报告已生 成，请相关同学查收！'))
    content = """
    各位好，本次电商项目测试报告执行如下：
    测试用例总数：110
    通过：100
    失败：5
    跳过：4
    异常：1
    点击查看测试报告：www.baidu.com
    """
    send_dingding_msg(content)



    # 注：截图此处截断，通常后续逻辑为：
    # 1. 构造请求头 headers = {'Content-Type': 'application/json'}
    # 2. 构造请求体 data = {"msgtype": "text", "text": {"content": content}, "at": {"isAtAll": at_all}}
    # 3. 使用 requests.post(url, json=data, headers=headers) 发送消息

