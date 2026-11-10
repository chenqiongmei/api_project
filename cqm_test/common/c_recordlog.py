import logging
import os
import time
from logging.handlers import RotatingFileHandler  # 按文件大小滚动备份
from conf import c_setting

# 1. 日志目录处理（跨平台）
log_path = c_setting.FILE_PATH['LOG']
if not os.path.exists(log_path):
    os.mkdir(log_path)

# 2. 日志文件名：按日期命名，使用 os.path.join 兼容 Mac/Windows
logfile_name = os.path.join(log_path, 'test.{}.log'.format(time.strftime("%Y%m%d")))

class RecordLog:
    """封装日志"""

    def output_logging(self):
        """获取logger对象，配置控制台与文件输出，防止重复添加"""
        # 获取以当前模块名命名的 logger
        logger = logging.getLogger(__name__)

        # 防止打印重复的 log 日志（多次调用 output_logging 时只添加一次）
        if not logger.handlers:
            # 设置日志级别（从配置读取，如 DEBUG/INFO）
            logger.setLevel(c_setting.LOG_LEVEL)

            # 日志格式：级别-时间-文件名:行号-[模块:函数名]-消息
            log_format = logging.Formatter(
                '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d - [%(module)s:%(funcName)s] - %(message)s'
            )

            # --- 文件输出 Handler（滚动切割） ---
            # maxBytes: 单个日志文件大小(5MB)，backupCount: 保留7个备份
            fh = RotatingFileHandler(filename=logfile_name, mode='a',
                                     maxBytes=5242880, backupCount=7,
                                     encoding='utf-8')
            fh.setLevel(c_setting.LOG_LEVEL)
            fh.setFormatter(log_format)
            logger.addHandler(fh)

            # --- 控制台输出 Handler（建议新增，方便本地调试） ---
            sh = logging.StreamHandler()
            sh.setLevel(c_setting.LOG_LEVEL)
            sh.setFormatter(log_format)
            logger.addHandler(sh)

        return logger


# 实例化调用（保持你原代码习惯，全局可直接 import apilog 使用）
apilog = RecordLog()
logs = apilog.output_logging()

