import re

from common.operyaml import get_testcase_yaml,ReadYamlData
import datetime
import random


class DebugTalk:

    def __init__(self):
        self.read = ReadYamlData()

    def get_extract_order_data(self, data, randoms):
        """获取extract.yaml数据，不为0、-1、-2，则按顺序读取文件key的数据"""
        if randoms not in [0, -1, -2]:
            return data[randoms - 1]

    def get_extract_data(self, node_name, randoms=None):
        """
        获取extract.yaml数据
        :param node_name: extract.yaml文件中的key值
        :param randoms: int类型，0：随机读取；-1：读取全部，返回字符串形式；-2：读取全部，返回列表形式；
        其他根据列表索引取值，取第一个值为1，第二个为2，以此类推;
        sec_node_name：extract.yaml有多层级时，获取下一个node节点的数据
        :return:
        """
        data = self.read.get_extract_yaml(node_name)
        if randoms is not None and bool(re.compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$').match(randoms)):
            randoms = int(randoms)
            data_value = {
                randoms: self.get_extract_order_data(data, randoms),
                0: random.choice(data),
                -1: ','.join(data),
                -2: ','.join(data).split(','),
            }
            data = data_value[randoms]
        else:
            data = self.read.get_extract_yaml(node_name, randoms)
        return data

    def get_extract_data_date(self):
        return 123456789

    def get_now_date(self):
        """
        获取当前日期的标准格式
        :return:
        """
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return now_time

    def replace_header(self, data_type):
        """动态替换请求头"""
        if data_type == 'data':
            return {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
        elif data_type == 'json':
            return {'Content-Type': 'application/json;charset=UTF-8'}

    def get_params(self):
        return 'test01'


if __name__ == '__main__':
    debug = DebugTalk()
    print(debug.get_extract_data('token'))
