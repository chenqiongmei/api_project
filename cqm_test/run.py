import pytest
import os
import allure
import shutil


if __name__ == '__main__':
    pytest.main()
    shutil.copy('./environment.xml', './report/temp')
    os.system(f'allure se rve ./report/temp')

# if __name__ == '__main__':
#     pytest.main()
#     os.system(f'allure serve ./report/temp')
    # pytest.main(['-vs', './testcase/Login/test_login.py'])



# if __name__ == '__main__':
#     pytest.main(['-vs', './testcase', '--alluredir=./report/temp', '--clean-alluredir'])
#     os.system('allure serve ./report/temp')




# 方式一：仅运行当前文件
# if __name__ == '__main__':
#     # 仅运行当前文件，并指定 allure 输出目录
#     pytest.main(['-vs', __file__, '--alluredir=./report/temp', '--clean-alluredir'])
#     # 可选：自动启动报告（需确保环境支持）
#     os.system('allure serve ./report/temp')
#
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






# if __name__ == '__main__':
#
#     # ========== 切换运行模式 ==========
#     RUN_MODE = 'single'  # 可选：'all' / 'module' / 'single'
#
#     if RUN_MODE == 'all':
#         # 运行所有用例
#         pytest.main(['-vs', './testcase', '--alluredir=./report/temp', '--clean-alluredir'])
#
#     elif RUN_MODE == 'module':
#         # 运行某个模块（目录）
#         pytest.main(['-vs', './testcase/Login', '--alluredir=./report/temp', '--clean-alluredir'])
#
#     elif RUN_MODE == 'single':
#         # 运行单个文件
#         pytest.main(['-vs', './testcase/Login/test_login.py', '--alluredir=./report/temp', '--clean-alluredir'])
#
#     # elif RUN_MODE == 'func':
#     #     # 运行单个函数
#     #     pytest.main(['-vs', './testcase/Login/test_login.py::TestLogin::test_case04',
#     #                  '--alluredir=./report/temp', '--clean-alluredir'])
#
#     else:
#         print("未知运行模式")
#
#     # 启动 Allure 报告
#     os.system('allure serve ./report/temp')


