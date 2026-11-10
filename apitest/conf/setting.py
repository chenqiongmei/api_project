import logging
import os
import sys

DIR_PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DIR_PATH)

# 设置日志级别
LOG_LEVEL = logging.DEBUG

# 设置控制台日志级别
STREAM_LOG_LEVEL = logging.DEBUG

API_TIMEOUT = 15

# 文件路径设置
FILE_PATH = {
    'YAML': os.path.join(DIR_PATH, 'testcase'),
    'CONFIG': os.path.join(DIR_PATH, 'conf/config.ini'),
    'EXTRACT': os.path.join(DIR_PATH, 'extract.yaml'),
    'LOG': os.path.join(DIR_PATH, 'log')
}
