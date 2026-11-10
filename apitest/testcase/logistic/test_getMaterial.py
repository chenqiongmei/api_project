import allure
import pytest

from base.apiutil import RequestBase
from base.generateId import m_id, c_id
from common.operyaml import get_testcase_yaml


@allure.feature(next(m_id) + '智慧物流项目')
class TestProductModule:

    @allure.story(next(c_id) + "获取物料信息")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("./testcase/logistic/getMaterial.yml"))
    def test_get_material(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)

    @allure.story(next(c_id) + "货主（托运人）下单")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("./testcase/logistic/xiadan.yml"))
    def test_xiadan(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)

    @allure.story(next(c_id) + "集团接收订单")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("./testcase/logistic/jiedan.yml"))
    def test_jiedan(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)

    @allure.story(next(c_id) + "集团分配物流公司")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("./testcase/logistic/fenpei.yml"))
    def test_fenpei(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)
