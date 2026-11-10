import os
import shutil,requests

import pytest

if __name__ == '__main__':
    pytest.main(['-s', '-v', '--alluredir=./report/temp', './testcase', '--clean-alluredir'])
    shutil.copy('./environment.xml', './report/temp')
    os.system(f'allure serve ./report/temp')
