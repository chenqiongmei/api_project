# -*- coding: utf-8 -*-
import json
import os
import yaml
import random
import time

# 动态推导项目根目录 (当前文件在 common/，向上两层即 cqm_test/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILE_PATH = {
    'c_extract': os.path.join(BASE_DIR, 'c_extract.yaml'),
    # 测试用例路径：根目录/testcase/Login/c_login.yaml
    'c_login': os.path.join(BASE_DIR, 'testcase', 'Login', 'c_login.yaml')
}
# 调试用：取消注释可验证路径
# print("BASE_DIR:", BASE_DIR)
# print("c_extract路径:", FILE_PATH['c_extract'])
# print("c_login路径:", FILE_PATH['c_login'])

def get_testcase_yaml(file):
    '''获取yaml文件数据'''
    try:
        with open(file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
            return yaml_data
    except Exception as e:
        print(f"读取YAML失败: {e}")
        return None


class ReadYamlData:
    def __init__(self, yaml_file=None):
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            self.yaml_file = FILE_PATH['c_login']

    def write_yaml_data(self, value):
        '''写入yaml文件'''
        file_path = FILE_PATH['c_extract']
        try:
            with open(file_path, 'a', encoding='utf-8') as file:
                if isinstance(value, dict):
                    write_data = yaml.dump(value, allow_unicode=True, sort_keys=False)
                    file.write(write_data)
                else:
                    print('写入数据必须为字典')
        except Exception as e:
            print(f"写入YAML失败: {e}")

    def get_extract_yaml(self, node_name):
        '''读取接口提取的变量值'''
        file_path = FILE_PATH['c_extract']
        if not os.path.exists(file_path):
            # 自动创建空yaml文件
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump({}, f)
            return None

        with open(file_path, 'r', encoding='utf-8') as rf:
            extract_data = yaml.safe_load(rf) or {}
            return extract_data.get(node_name)

    def get_extract_data(self, node_name, randoms=None):
        '''获取extract.yaml的数据，支持随机/拼接/按序号取'''
        data = self.get_extract_yaml(node_name)
        if data is None:
            return None

        if randoms is not None:
            try:
                randoms = int(randoms)
            except (ValueError, TypeError):
                return data

            if randoms == 0:
                return random.choice(data) if isinstance(data, list) and data else data
            elif randoms == -1:
                return ','.join(str(d) for d in data) if isinstance(data, list) else str(data)
            elif randoms == -2:
                return list(data) if isinstance(data, list) else [data]
            elif 1 <= randoms <= len(data):
                return data[randoms - 1]
            else:
                return data

        return data

    def get_extract_order_data(self, data, randoms):
        '''列表数据按规则取值'''
        try:
            randoms = int(randoms)
        except (ValueError, TypeError):
            return data

        if randoms == 0:
            return random.choice(data) if data else None
        elif randoms == -1:
            return ','.join(str(d) for d in data)
        elif randoms == -2:
            return list(data)
        elif 1 <= randoms <= len(data):
            return data[randoms - 1]
        else:
            return data

    def clear_yaml_data(self):
        """
        清空c_extract.yaml文件的数据
        :return:
        """
        with open(FILE_PATH['c_extract'],'w') as f:
            f.truncate()




if __name__ == '__main__':
    # 获取 c_read_yaml.py 所在目录 (common)，再往上推到项目根目录 (cqm_test)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 拼接真实路径（注意统一小写 login，以你实际目录为准）
    yaml_path = os.path.join(BASE_DIR, 'testcase', 'login', 'c_login.yaml')
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
    # print(res)
    # print(new_url)
    # print(data)

    from common.c_sendrequests import SendRequests
    send = SendRequests()
    res = send.run_main(url = new_url, data=data, header=None, method=method)
    print(res)
    # print(type(res))
    json_str = json.dumps(res,ensure_ascii=False)
    # print(json_str)
    # print(type(json_str))

    token = res.get('token')
    write_data = {}
    write_data['Token'] = token # 注意字典取键值
    print(token)
    read = ReadYamlData()
    read.write_yaml_data(write_data)


    # python常用数据类型：str list dict set tuple
    # json 序列化（字典转json）、反序列化(json转字典)

    

