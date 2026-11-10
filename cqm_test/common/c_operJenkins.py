import json
import re
import jenkins
# 首先需要安装：pip install python-jenkins
from conf.c_operationConfig import OperationConfig

# 实例化配置操作类，用于读取 config.ini 中的配置
conf = OperationConfig()

class OperJenkins:
    """读取Jenkins持续集成的测试报告"""

    def __init__(self):
        # 从配置文件的 [JENKINS] 区块读取配置，组装为字典
        # 注：timeout 转为 int 类型
        self.__config = {
            'url': conf.get_section_jenkins('url'),
            'username': conf.get_section_jenkins('username'),
            'password': conf.get_section_jenkins('password'),
            'timeout': int(conf.get_section_jenkins('timeout'))
        }
        # 初始化 Jenkins 连接实例（解包配置字典传入）
        # 对应上轮提到的 jenkins.Jenkins(...)
        self.__server = jenkins.Jenkins(**self.__config)

        # 获取到Jenkins上的项目名（从配置读取 job_name）
        self.job_name = conf.get_section_jenkins('job_name')

    def get_job_number(self):
        """读取jenkins job构建号"""
        # 获取最后一次构建(lastBuild)的编号(number)
        build_number = self.__server.get_job_info(self.job_name).get('lastBuild').get('number')
        return build_number

    def get_build_job_status(self):
        """读取构建完成的状态"""
        # 先获取最新构建号，再查询该次构建的结果(result)
        # 结果通常为 'SUCCESS', 'FAILURE', 'UNSTABLE', 'ABORTED' 或 None(构建中)
        build_num = self.get_job_number()
        job_status = self.__server.get_build_info(self.job_name, build_num).get('result')
        return job_status

    def get_console_log(self):
        """获取控制台日志"""
        # 获取该任务最新构建的控制台输出文本
        console_log = self.__server.get_build_console_output(self.job_name, self.get_job_number())
        return console_log

    def get_job_description(self):
        """返回job描述信息"""
        # 获取任务描述(description)和任务访问链接(url)
        description = self.__server.get_job_info(self.job_name).get('description')
        url = self.__server.get_job_info(self.job_name).get('url')
        return description, url

    def get_build_report(self):
        """返回第n次构建的测试报告"""
        # 调用 Jenkins API 获取测试报告（通常需 Jenkins 安装 JUnit/TestNG 插件并配置报告路径）
        report = self.__server.get_build_test_report(self.job_name, self.get_job_number())
        return report

    def report_success_or_fail(self):
        """统计测试报告用例成功数、失败数、跳过数以及成功率、失败率"""
        # 获取测试报告数据（包含 pass/fail/skip 等统计）
        report_info = self.get_build_report()

        # 提取测试报告链接（通过正则从控制台日志中匹配 Allure 报告地址）
        # 注：正则 r'http://192.168.*/job/jjapi/(.*?)allure' 为示例，需按实际网络环境调整
        console_log = self.get_console_log()
        report_line = re.search(r'http://192.168.*/job/jjapi/(.*?)allure', console_log).group(0)

        return report_line
        # 注：截图在此处截断。实际完整逻辑通常还会解析 report_info 中的用例数，
        # 并结合历史 dingRobot 发送钉钉通知（如：总用例数、通过数、失败数、报告链接等）


