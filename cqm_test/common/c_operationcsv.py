import csv
import os
from conf.c_setting import DIR_PATH
from common.c_recordlog import logs

def read_csv_data(file_name):
    """
    读取csv文件数据
    :param file_name:csv文件名
    :return:
    """
    # 'data'：项目根目录下，data文件夹
    try:
        with open(os.path.join(DIR_PATH,'data',file_name),'r',encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            for value in csv_reader:
                print(value)
            return csv_reader
    except Exception as e:
        logs.error(e)


if __name__ == '__main__':


