import time

import pytest

class TestSystem:

    def test_case01(self):
        time.sleep(1)
        print('系统管理1')

    def test_case02(self):
        time.sleep(1)
        print('系统管理2')

if __name__ == '__main__':
    pytest.main()