# -*- coding: utf-8 -*-
import os
import logging
import time
from logging.handlers import RotatingFileHandler
import datetime
import colorlog

from conf import setting

LOG_PATH = setting.FILE_PATH["LOG"]
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

LOG_FILE_NAME = os.path.join(LOG_PATH, f"test.{time.strftime('%Y%m%d')}.log")


def handle_overdue_log():
    """处理过期日志文件"""
    now_time = datetime.datetime.now()
    offset_date = datetime.timedelta(days=-30)
    before_date = (now_time + offset_date).timestamp()
    files = os.listdir(LOG_PATH)
    for file in files:
        if os.path.splitext(file)[1]:
            filepath = os.path.join(LOG_PATH, file)
            file_create_time = os.path.getctime(filepath)
            if file_create_time < before_date:
                os.remove(filepath)


def log_color():
    """设置日志颜色"""
    log_color_config = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red'
    }
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s %(levelname)s - %(asctime)s - %(filename)s:%(lineno)d -[%(module)s:%(funcName)s] - %(message)s',
        log_colors=log_color_config)
    return formatter


def init_logging(log_level=logging.DEBUG, stream_log_level=logging.INFO):
    """获取logger对象并初始化"""
    logger = logging.getLogger(__name__)
    stream_format = log_color()

    if not logger.handlers:
        logger.setLevel(log_level)
        log_format = logging.Formatter(
            '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d -[%(module)s:%(funcName)s] - %(message)s')
        fh = RotatingFileHandler(filename=LOG_FILE_NAME, mode='a', maxBytes=5242880,
                                 backupCount=7,
                                 encoding='utf-8')
        fh.setLevel(log_level)
        fh.setFormatter(log_format)
        logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setLevel(stream_log_level)
        sh.setFormatter(stream_format)
        logger.addHandler(sh)

    return logger


class RecordLog:
    """日志模块"""

    def __init__(self):
        handle_overdue_log()

    def output_logging(self):
        """获取logger对象"""
        return init_logging()


apilog = RecordLog()
logs = apilog.output_logging()
