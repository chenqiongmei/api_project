import os

import yaml

from conf.setting import FILE_PATH


def get_testcase_yaml(file):
    testcase_list = []
    with open(file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        if len(data) <= 1:
            yam_data = data[0]
            base_info = yam_data.get('baseInfo')
            for ts in yam_data.get('testCase'):
                param = [base_info, ts]
                testcase_list.append(param)
            return testcase_list
        else:
            return data


class ReadYamlData(object):

    def write_yaml_data(self, value):
        file = None
        file_path = FILE_PATH['EXTRACT']
        if not os.path.exists(file_path):
            os.system(file_path)

        try:
            file = open(file_path, 'a', encoding='utf-8')
            if isinstance(value, dict):
                write_data = yaml.dump(value, allow_unicode=True, sort_keys=False)
                file.write(write_data)
            else:
                print('写入到[extract.yaml]的数据必须是字典类型格式！')
        except Exception as e:
            print(e)
        finally:
            file.close()

    def get_extract_yaml(self, node_name, second_node_name=None):
        """
        用于读取接口提取的变量值
        :param node_name:
        :return:
        """
        if os.path.exists(FILE_PATH['EXTRACT']):
            pass
        else:
            print('extract.yaml不存在')
            file = open(FILE_PATH['EXTRACT'], 'w')
            file.close()
            print('extract.yaml创建成功！')
        try:
            with open(FILE_PATH['EXTRACT'], 'r', encoding='utf-8') as rf:
                ext_data = yaml.safe_load(rf)
                if second_node_name is None:
                    return ext_data[node_name]
                else:
                    return ext_data[node_name][second_node_name]
        except Exception as e:
            print(f"【extract.yaml】没有找到：{node_name},--%s" % e)

    def clear_extract_yaml(self):
        """
        清除extract.yaml文件的数据
        :return:
        """
        with open(FILE_PATH['EXTRACT'], 'w') as f:
            f.truncate()


if __name__ == '__main__':
    print(get_testcase_yaml('../testcase/publicApi/addUser.yaml'))
    # read = ReadYamlData()
    # value = {'name': '哈哈'}
    # read.write_yaml_data(value)
