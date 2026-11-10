import pytest
import time
import os
from common.c_sendrequests import SendRequests
from common.c_read_yaml import get_testcase_yaml
from common.c_recordlog import logs
from base.c_apiutil import RequestsBase
import allure


# # 该方法统一写入 conftest.py文件
# @pytest.fixture(scope="class", params=['北京', '广州', '深圳'], autouse=True, ids=['BJ', 'GZ', 'SZ'], name="")   # 实现用例前后置，实现用例前后置：如①登录；②清除文件
# def fixture_test(request):
#     """前后置处理"""
#     print("---------接口测试开始---------")
#     yield      # yield前的代码可返回；yield后的代码只做清理，不返回
#     print("---------接口测试结束 ---------")
#     return request.param
# 输出测试报告左侧测试用例树
@allure.feature('登录接口')
class TestLogin:
    YAML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'c_login.yaml')
    # @classmethod
    # def setup_class(cls):
    #     """类级前置：在所有case执行前都先1次"""
    #     print("类的初始化工作：如创建对象、创建数据可连接")
    #
    # def setup_method(self):
    #     """方法级前置：每个case执行前都先执行1次"""
    #     print("前置处理：每个case执行前都先执行1次")

    # @pytest.mark.run(order=2)
    # @pytest.mark.parametrize('params', ['小米', '小红', '小宝'])  # 列表
    # @pytest.mark.parametrize('params', ('小米', '小红', '小宝'))  # 元组
    # @pytest.mark.parametrize('params',{'name': '小米'}, {'name': '小红'})  # 字典
    # @pytest.mark.parametrize('params',({'name': '小米'}, {'name': '小红'}))  # 字典元组

    # 绝对路径（视频用相对路径是因为他rootdir刚好，你用这个永不踩坑）
    # YAML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'c_login.yaml')
    # @pytest.mark.parametrize('params', get_testcase_yaml(YAML_PATH))
    # def test_case01(self, params):
    #     url = params['baseInfo']['url']
    #     new_url = 'http://127.0.0.1:8787' + str(url)
    #     # c_recordlog.logs输出日志
    #     # logs.info("获取到的接口地址：%s", new_url)
    #     logs.info("获取到的接口地址：{}".format(new_url))
    #     print(new_url)
    #     method = params['baseInfo']['method']
    #     logs.info("获取到的接口方法：{}".format(method))
    #     # print(method)
    #     headers = params['baseInfo']['header']
    #     # print(headers)
    #     data = params['testCase'][0]['data']
    #     logs.info("获取到的接口参数：{}".format(data))
    #     print(data)
    #     send = SendRequests()
    #     res = send.run_main(url=new_url, data=data, header=None, method=method)
    #     logs.info("获取到的接口返回值：{}".format(res))
    #     print(res)
    #     # time.sleep(1)
    #     # print('我是第2个执行：pytest测试框架')
    #     # print('获取到的参数为：', params)
    #     assert res['msg'] == '登录成功'

    # @pytest.mark.smoke
    # @pytest.mark.run(order=1)
    # @pytest.mark.parametrize('params', get_testcase_yaml(YAML_PATH))
    # def test_case_02(self, params):
    #     url = params['baseInfo']['url']
    #     new_url = 'http://127.0.0.1:8787' + str(url)
    #     print(new_url)
    #     method = params['baseInfo']['method']
    #     print(method)
    #     headers = params['baseInfo']['header']
    #     print(headers)
    #     data = {'user_name': 'test01', 'passwd': 'admin123'}
    #     print(data)
    #     send = SendRequests()
    #     res = send.run_main(url=new_url, data=data, header=None, method=method)
    #     print(res)
    #     time.sleep(1)
    #     print('我是第1个执行：pytest运行方式')
    #     assert res['msg']== '登录成功'

    # @pytest.mark.skip
    # @pytest.mark.run(order=3)
    # 调用前后置方法fixture_test里的参数
    # def test_case_03(self, fixture_test):
    #     time.sleep(1)
    #     print('我是第3个执行：pytest测试')
    #     print("获取前置用例的参数：", fixture_test)

    # def teardown_method(self):
    #     """方法级后置:每个case执行后都先执行1次"""
    #     print("后置处理：每个case执行后都先执行1次")
    #
    # def teardown_class(cls):
    #     """类级后置：在所有case执行前都先1次"""
    #     print("类的初始化工作：如关闭数据可连接")

    @allure.story('用户名密码正确')
    # @allure.title('登录成功-用户名密码正确')  # 强制左侧显示此中文
    @pytest.mark.parametrize('params', get_testcase_yaml(YAML_PATH))
    def test_case04(self, params):
        # allure.dynamic.title(params.get('title', '默认标题'))  # 动态取中文
        RequestsBase().specification_yaml(params)

    @allure.story('用户名or密码错误')
    # @allure.title('登录失败-用户名or密码错误')  # 强制左侧显示此中文
    @pytest.mark.parametrize('params', get_testcase_yaml(YAML_PATH))
    def test_case05(self, params):
        # allure.dynamic.title(params.get('title', '默认标题'))  # 动态取中文
        RequestsBase().specification_yaml(params)

# # 方式一：仅运行当前文件
# if __name__ == '__main__':
#     # 仅运行当前文件，并指定 allure 输出目录
#     pytest.main(['-vs', __file__, '--alluredir=./report/temp', '--clean-alluredir'])
#     # 可选：自动启动报告（需确保环境支持）
#     os.system('allure serve ./report/temp')
#
# # 方式二（推荐）：基于当前文件绝对定位，确保任何情况只跑本目录
# if __name__ == '__main__':
#     import os
#     # 锁定 productManager 目录
#     target_dir = os.path.dirname(os.path.abspath(__file__))
#     pytest.main(['-vs', target_dir, '--alluredir=./report/temp', '--clean-alluredir'])
#     os.system('allure serve ./report/temp')
#
# # 方式三：运行testcase下的文件夹中的test开头的py文件
# if __name__ == '__main__':
#     # 直接指向 testcase 根目录，pytest 默认递归收集所有 test_*.py
#     pytest.main(['-vs', './testcase', '--alluredir=./report/temp', '--clean-alluredir'])
#     os.system('allure serve ./report/temp')

    # 运行方法：
    # ①主函数运行方式；
# if __name__ == '__main__':
#     pytest.main(['-vs', __file__])

    # ②命令行运行方式；
    # 直接终端输入：pytest，分组执行
    # pytest -vs ./testcase -m "maoyan or usermanager"

    # ③通过读取pytest.ini配置文化

