import time

import pytest

class TestAddUser:

    # 分组执行用例
    @pytest.mark.usermanager
    @pytest.mark.run(order=1)
    def test_case01(self):
        time.sleep(1)
        print('新增用户')

    @pytest.mark.parametrize('params', ['小米', '小红', '小宝'])  # 列表
    # @pytest.mark.parametrize('params', ('小米', '小红', '小宝'))  # 元组
    # @pytest.mark.parametrize('params',{'name': '小米'}, {'name': '小红'})  # 字典
    # @pytest.mark.parametrize('params',({'name': '小米'}, {'name': '小红'}))  # 字典元组
    def test_case02(self, params):
        time.sleep(1)
        print('删除用户')
        print(params)

    def test_case03(self):
        time.sleep(1)
        print('修改用户')

if __name__ == '__main__':
        pytest.main()