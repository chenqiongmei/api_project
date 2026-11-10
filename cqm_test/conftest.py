import pytest
import time
from common.c_recordlog import logs
from common.c_read_yaml import ReadYamlData
from common.c_dingRobot import send_dingding_msg
from common.c_operJenkins import OperJenkins

# '''
# function: 每一个函数方法都会调用
# class: 每一个类调用一次，一个类中可以有多个方法
# module: 每一个.py文件调用一次，该文件内只有多个function和class
# session: 多个文件调用一次，可以跨.py文件调用，每个.py文件就是module，整个目录只会运行一次
# autouse: 默认为False，不会自动执行，需要手动调用，为True可以自动执行，不需要调用
# yield: 前置、后置
# '''


read=ReadYamlData
@pytest.fixture(scope="session",  autouse=True)
def clear_extract_data():
    read.clear_yaml_data()


@pytest.fixture(scope="session",  autouse=True)   # 实现用例前后置：如①登录；②清除文件
def fixture_test(request):
    """前后置处理"""
    print("---------接口测试开始---------")
    logs.info('---------接口测试开始---------')
    yield      # yield前的代码可返回；yield后的代码只做清理，不返回
    print("---------接口测试结束 ---------")
    logs.info("---------接口测试结束 ---------")
    # print('获取到的参数为：', params)
    # 仅当 Fixture 被“参数化”时，即装饰器里必须有 params=[...]，才return
    # return request.param

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    pytest_terminal_summary 是 Pytest 提供的生命周期钩子函数，函数名不可变更，测试结束打印摘要时自动触发，适合做结果汇总与第三方通知
    每次pytest测试完成后，会自动收集测试结果的数据（Pytest内置钩子函数）
    :param terminalreporter: 内部终端报告对象，对象的stats属性包含各状态用例
    :param exitstatus: 将报告回操作系统的退出状态
    :param config: pytest配置对象
    :return:
    """
    # 打印原始统计信息（调试用）
    print(terminalreporter.stats)

    # 收集测试用例总数（下划线开头为内部属性，通常可用，但部分版本建议用 config 获取）
    case_total = terminalreporter._numcollected
    print(f'测试用例总数：{case_total}个')

    # 收集测试用例通过数（从 stats 中取 'passed' 列表，默认空列表防None）
    passed = len(terminalreporter.stats.get('passed', []))
    print(f'通过数：{passed}个')

    # 收集测试用例失败数
    failed = len(terminalreporter.stats.get('failed', []))
    print(f'失败数：{failed}个')

    # 收集测试用例错误数量
    error = len(terminalreporter.stats.get('error', []))
    print(f'错误数：{error}个')

    # 收集测试用例跳过执行数
    skipped = len(terminalreporter.stats.get('skipped', []))
    print(f'跳过执行数：{skipped}个')

    # 收集测试用例执行时长（当前时间 - 会话开始时间）
    duration = time.time() - terminalreporter._sessionstarttime
    print(f'测试用例执行时长：{duration}')
    # 拼接钉钉通知文本（f-string 多行格式化）
    # 注：截图3中 {duration} 后缺冒号/单位，此处补全为时长秒数展示
    oper=OperJenkins()
    report=oper.report_success_or_fail()
    content = f"""
各位好，本次XXX置灰物流项目的接口自动化测试结果如下，请注意失败及错误的接口：
测试用例总数：{case_total}个
通过数：{passed}个
失败数：{failed}个
跳过执行数：{skipped}个
错误异常：{error}个
测试用例执行时长：{duration:.2f}秒
点击查看测试报告：{report}
""".strip()  # strip() 去除首尾换行，使钉钉展示更紧凑

    # 调用钉钉机器人发送消息（需确保 dingRobot.py 中的 send_dingding_msg 已导入）
    send_dingding_msg(content=content)

# 注：截图1底部的 pytest_terminal_summary() 为误写，钩子函数由pytest自动调用，无需手动调用