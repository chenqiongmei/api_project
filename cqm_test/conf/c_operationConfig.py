# 从 conf 目录下的 setting 模块导入 FILE_PATH 字典（如历史代码中的路径配置）
from conf.c_setting import FILE_PATH
# 导入 Python 标准库 configparser，用于读取 ini 配置文件
import configparser
import os

class OperationConfig:
    """封装读取ini配置文件"""

    def __init__(self, file_path=None):
        # 如果未传入文件路径，则默认使用 FILE_PATH 字典中 'conf' 对应的路径
        if file_path is None:
            self.__file_path = FILE_PATH['conf']
        else:
            self.__file_path = file_path

        # 实例化 ConfigParser 对象
        self.conf = configparser.ConfigParser()
        try:
            # 读取 ini 文件，指定编码为 utf-8 防止乱码
            self.conf.read(self.__file_path, encoding='utf-8')
            print("实际读取路径:", self.__file_path)
            print("文件是否存在:", os.path.exists(self.__file_path))
            print("文件大小:", os.path.getsize(self.__file_path) if os.path.exists(self.__file_path) else 0)
            self.conf.read(self.__file_path, encoding='utf-8')
            print("读取到的节点:", self.conf.sections())  # 如果为空列表，说明没读到
        except Exception as e:
            # 捕获并打印读取异常（如文件不存在）
            print(e)

    def get_section_for_data(self, section, option):
        """
        读取ini数据
        :param section: ini头部值（即 [section]）
        :param option: 选项值的key（即 key=value 中的 key）
        :return: 返回对应的值
        """
        try:
            # 获取指定 section 下的 option 值
            data = self.conf.get(section, option)
            return data
        except Exception as e:
            # 捕获并打印异常（如 section 或 option 不存在）
            print(e)

    def get_envi(self, option):
        """获取接口服务器ip地址"""
        # 固定读取 'api_envi' 区块下的指定 option
        return self.get_section_for_data('api_envi', option)

    def get_mysql_conf(self, option):
        return self.get_section_for_data('MASQL', option)

    def get_api_host(self):
        return self.get_section_for_data('api_envi', 'host')

    def get_section_jenkins(self, option):
        return self.get_section_for_data('JENKINS', option)

if __name__ == '__main__':
    # 实例化对象（使用默认配置文件）
    oper = OperationConfig()
    # 打印输出文件 c_conf.ini 'api_envi' 下 'host' 的值
    print(oper.get_envi('host'))