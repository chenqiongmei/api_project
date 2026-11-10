import os
import sys
import logging

# ================= 1、项目路径配置（跨平台核心） =================
# # 当前文件所在目录 → .../cqm_test/conf/
CONF_DIR = os.path.dirname(os.path.abspath(__file__))
# print("conf目录:", CONF_DIR)

# 项目根目录 → .../cqm_test/（conf 的上级目录）
DIR_PATH = os.path.dirname(CONF_DIR)
# print("项目根目录:", DIR_PATH)

# 加入 sys.path，保证模块互相 import 正常
sys.path.append(DIR_PATH)

# ================= 2. 文件路径配置 =================
FILE_PATH = {
    # ---------- YAML ----------
    'c_extract': os.path.join(DIR_PATH, 'c_extract.yaml'),
    'c_login_yaml': os.path.join(DIR_PATH, 'testcase', 'Login', 'c_login.yaml'),

    # ---------- 配置文件 ----------
    'conf': os.path.join(DIR_PATH, 'conf', 'c_conf.ini'),

    # ---------- 日志 / 报告 / 数据 ----------
    'LOG': os.path.join(DIR_PATH, 'log'),
    'REPORT': os.path.join(DIR_PATH, 'report'),
    'DATA': os.path.join(DIR_PATH, 'data'),
# 可继续扩展 'CONF': CONF_DIR 等
}
# print("conf文件路径:", FILE_PATH['conf'])
# print("extract文件路径:", FILE_PATH['c_extract'])

# ================= 3. 日志配置 =================
# log输出日志级别
# 写入文件级别（logging 常量，整数）
# 使用 logging 模块常量（整数），recordlog.py 中 setLevel() 直接传此值
LOG_LEVEL = logging.DEBUG
# 控制台输出级别
STREAM_LOG_LEVEL = logging.DEBUG

# 日志级别（DEBUG / INFO / WARNING / ERROR）
# 注意：实际日志文件名(带日期)在 recordlog.py 中拼接，这里只给目录
# recordlog.py 中建议：logfile_name = os.path.join(setting.FILE_PATH['LOG'], f"test.{time_str}.log")

# ================= 4.其他配置（示例） =================
# 接口请求相关
# API_BASE_URL = "http://xxx"


# ================= 4. 调试入口（直接运行本文件验证） =================
if __name__ == '__main__':
    print("=" * 60)
    print("c_setting.py 路径配置验证")
    print("=" * 60)
    print(f"conf目录:     {CONF_DIR}")
    print(f"项目根目录:   {DIR_PATH}")
    print()
    print("文件路径清单:")
    for key, path in FILE_PATH.items():
        print(f"  {key:15s} → {path}")
    print("=" * 60)


# ================= 调试入口 =================
if __name__ == '__main__':
    print("conf目录:", CONF_DIR)
    print("项目根目录:", DIR_PATH)
    print()
    for key, path in FILE_PATH.items():
        exists = os.path.exists(path)
        status = "YES" if exists else "📁(将自动创建)" if "DIR" in key or key in ('LOG', 'REPORT', 'DATA') else "NO"
        print(f"  {key:15s} → {path}  {status}")






