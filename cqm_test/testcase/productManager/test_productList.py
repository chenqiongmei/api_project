import allure
import os
import pytest
from common.c_read_yaml import get_testcase_yaml
from base.c_apiutil import RequestsBase

@allure.feature('商品管理')
class TestProduct:
    YAML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'getProductList.yaml')

    @allure.story('获取商品列表')
    @pytest.mark.parametrize('params', get_testcase_yaml(YAML_PATH))
    def test_get_product_list(self, params):
        # allure.dynamic.title(params.get('title', '默认标题'))  # 动态取中文
        RequestsBase().specification_yaml(params)

    @allure.story('获取商品详情')
    @pytest.mark.parametrize('params', get_testcase_yaml(YAML_PATH))
    def test_get_product_detail(self, params):
        # allure.dynamic.title(params.get('title', '默认标题'))  # 动态取中文
        RequestsBase().specification_yaml(params)


# 方式一：仅运行当前文件
if __name__ == '__main__':
    # 仅运行当前文件，并指定 allure 输出目录
    pytest.main(['-vs', __file__, '--alluredir=./report/temp', '--clean-alluredir'])
    # 可选：自动启动报告（需确保环境支持）
    os.system('allure serve ./report/temp')

#  # 方式二（推荐）：基于当前文件绝对定位，确保任何情况只跑本目录
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