# -*- coding: utf-8 -*-
import json
import yaml
import os
from conf.c_setting import FILE_PATH
import random
from common.c_sendrequests import SendRequests


def get_testcase_yaml(file):
    '''
    获取yaml文件数据
    :param file: yaml文件路径
    :return:
    '''
    # .safe_load 将 YAML 格式的文本流，转换成 Python 原生的数据结构（如字典 dict、列表 list、字符串等）
    try:
        with open(file,'r',encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
            return yaml_data
    except Exception as e:
        print(e)

class ReadYamlData:
    '''
    读取yaml文件并写入数据
    :return:初始化实例属性
    '''
    def __init__(self,yaml_file=None):
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            self.yaml_file = '../../../cqm_test/testcase/Login/c_login.yaml'

    def write_yaml_data(self,value):
        '''
        写入yaml文件
        :param value:
        :return:
        '''
        file=None
        # file_path = r'c_extract.yaml'
        file_path = FILE_PATH['c_extract']

        # if not os.path.exists(file_path):
        #     os.system(file_path)  # 无该文件则创建
        try:
            file = open(file_path,'a',encoding='utf-8') # "a"为追加，无则自动创建;"w"清空后覆盖写入
            if isinstance(value,dict):
                write_data=yaml.dump(value,allow_unicode=True,sort_keys=False)
                file.write(write_data)
            else:
                print('写入【c_extract.yamle】文件的数据必须为字典')
        except Exception as e:
            print(e)
        finally:
            file.close()

    def get_extract_yaml(self,node_name):
        """
        读取接口提取的变量值
        :param node_name:
        :return:
        """
        if os.path.exists('../../../cqm_test/c_extract.yaml'):
            pass
        else:
            print('c_extract.yaml不存在')
            file = open('../../../cqm_test/c_extract.yaml','w')
            file.close()
            print('c_extract.yaml 创建成功')

        with open('../../../cqm_test/c_extract.yaml','r',encoding='utf-8') as rf:
            extract_data = yaml.safe_load(rf)
            return extract_data[node_name]


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


    def get_extract_data(self,node_name,randoms=None):
        """
         获取extract.yaml的数据
        :param node_name: extract.yaml中的key值
        :param randoms: 随机读取（0:随机单条, -1:拼接全部, 其他:原数据）
        :return:
        """
        data = self.read.get_extract_yaml(node_name)
        if randoms is not None:
            randoms = int(randoms)  # 数值类型，
            data_value = {
                0: random.choice(data),  # 字典的键是 0，值是随机取的数据
                -1: ','.join(data),
                -2:  ','.join(data).split(',')
                         }
            data = data_value[randoms]
        return data


if __name__ == '__main__':
    # 获取 c_read_yaml.py 所在目录 (common)，再往上推到项目根目录 (cqm_test)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 拼接真实路径（注意统一小写 login，以你实际目录为准）
    yaml_path = os.path.join(BASE_DIR, 'testcase', 'login', 'c_loginlogin.yaml')
    # 或者直接写死完整路径（仅本地调试用）
    # yaml_path = '/Users/chengqiongmei/Downloads/pytest/api_project/cqm_test/testcase/login/c_login.yaml'
    res = get_testcase_yaml(yaml_path)[0]
    # ... 后续代码

    # res = get_testcase_yaml('/testcase/Login/c_login.yaml')[0]
    method = res['baseInfo']['method']
    url = res['baseInfo']['url']
    new_url = 'http://127.0.0.1:8787' + url
    data = res['baseInfo']['testCase'][0]['data']
    first_case = res['baseInfo']['testCase'][0]['case_name']  # 取第1个用例名
    print(res)
    # print(new_url)
    # print(data)

    from common.c_sendrequests import SendRequests
    send = SendRequests()
    res = send.run_main(url = new_url, data=data, header=None, method=method)
    print(res)
    print(type(res))
    json_str = json.dumps(res,ensure_ascii=False)
    print(json_str)
    print(type(json_str))


    token = res.get('token')
    write_data = {}
    write_data['Token'] = token # 注意字典取键值
    print(token)
    read = ReadYamlData()
    read.wirte_yaml_data(write_data)



    # python常用数据类型：str list dict set tuple
    # json 序列化（字典转json）、反序列化(json转字典)

    

