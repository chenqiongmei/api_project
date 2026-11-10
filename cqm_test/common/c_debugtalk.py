import random
from common.c_read_yaml import ReadYamlData
import time
import random

class DebugTalk:

    def __init__(self):
        # 核心修复：必须加括号实例化，确保 self.read 存在
        self.read = ReadYamlData()

    def get_extract_order_data(self, data, randoms):
        """
        :param data: 列表数据，如 ["-12", "-34", "-56"]
        :param randoms: 0:随机单条, -1:拼接全部, -2:返回列表, 正整数n:取第n条(1开始)
        :return:
        """
        # 确保 randoms 是数字（防止 YAML 传字符串）
        try:
            randoms = int(randoms)
        except (ValueError, TypeError):
            return data  # 转换失败返回原数据

        # 特殊逻辑：0, -1, -2
        if randoms == 0:
            return random.choice(data) if data else None
        elif randoms == -1:
            return ','.join(str(d) for d in data)  # 拼接："-12,-34,-56"
        elif randoms == -2:
            return list(data)  # 返回原列表

        # 其他情况：按序号取（1代表第1个，2代表第2个）
        # 防止越界：校验范围
        if 1 <= randoms <= len(data):
            return data[randoms - 1]
        else:
            # 超出范围或负数（非-1/-2），返回原数据或抛异常
            return data  # 或者 raise IndexError("序号超出范围")

    def get_extract_data_list(self,node_name,randoms=None):
        """
         获取extract.yaml的数据
        :param node_name: extract.yaml中的key值
        :param randoms: （int类型，0:随机单条, -1:拼接全部, 其他:原数据）
        :return:
        """
        data = self.read.get_extract_yaml(node_name)
        if randoms is not None:
            randoms = int(randoms)  # 数值类型，
            data_value = {
                0: random.choice(data),  # 字典的键是 0，值是随机取的数据
                -1: ','.join(data),
                -2: ','.join(data).split(',')
            }
            data = data_value[randoms]
        return data

    def get_extract_data(self,node_name,sec_node_name=None):
        """
         获取extract.yaml的数据
        :param node_name: extract.yaml中的key值
        :param sec_node_name:extract.yaml中的key值
        :param randoms: （int类型，0:随机单条, -1:拼接全部, 其他:原数据）
        :return:
        """
        data = self.read.get_extract_yaml(node_name,sec_node_name)
        print("data的值从c_extract.yaml文件读取：",data)
        return data



    def get_stamp_time(self):
        """秒级时间戳（整数，如 1762416000）"""
        return int(time.time())

    def md5_params(self,params):
        print('实现md5加密')
        return 'ABCD1234' + str(params)


if __name__ == '__main__':
    debug = DebugTalk()  # 这里触发 __init__
    print(debug.get_extract_data('product_id', -1))
    print(debug.get_extract_data('product_id',-2))
    print(debug.get_extract_data('product_id', 0))
