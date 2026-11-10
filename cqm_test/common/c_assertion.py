import operator
import os.path
import allure
import jsonpath
from common.c_recordlog import logs
from common.c_connection import ConnectMysql

class Assertions:
    """
    接口断言模式封装，支持
    1. 字符串包含
    2. 结果相等断言
    3. 结果不相等断言
    4. 断言接口返回值里面的任意一个值
    5. 数据库断言
    """

    def contains_assert(self, value, response, status_code):
        """
        第一种模式，字符串包含断言，断言预期结果的字符串是否包含在接口的实际返回结果当中
        :param value: 预期结果，yaml文件当中validation关键字下面的参数
        :param response: 接口的实际返回结果
        :param status_code: 接口的实际返回状态码
        :return: flag标识，0表示成功，非0表示失败
        """
        flag = 0
        for assert_key, assert_value in value.items():
            # 单独校验状态码
            if assert_key == 'status_code':
                if assert_value != status_code:
                    flag += 1
                    # Allure 报告附加错误信息
                    allure.attach(f'预期结果：{assert_value}\n实际结果：{status_code}', '响应代码断言失败',
                                  allure.attachment_type.TEXT)
                    logs.error('contains断言失败，接口返回的[%s]不等于[%s]' % (status_code, assert_value))
            else:
                # 使用 jsonpath 提取实际返回中对应字段的值（支持深层提取）
                resp_list = jsonpath.jsonpath(response, '$..%s' % assert_key)
                if isinstance(resp_list, list):
                    # 若提取结果为列表且是字符串，拼接成单字符串便于包含判断
                    if isinstance(resp_list[0], str):
                        resp_list = ''.join(resp_list)
                    if resp_list:
                        # 判断预期值是否在实际提取结果中
                        if assert_value in resp_list:
                            logs.info('字符串包含断言成功：预期结果为：[%s]，实际结果为：[%s]' % (assert_value, resp_list))
                        else:
                            flag += 1
                            logs.error('响应文本字符串包含断言失败：预期结果为：[%s]，实际结果为：[%s]' % (
                            assert_value, resp_list))
                            allure.attach(f'预期结果：{assert_value}\n实际结果：{resp_list}',
                                          '响应文本字符串包含断言失败',
                                          allure.attachment_type.TEXT)
                    else:
                        # jsonpath 提取为空（路径不存在）
                        flag += 1
                        logs.error('响应文本字符串包含断言失败：提取字段[%s]不存在' % assert_key)
                else:
                    # jsonpath 返回 False 表示未找到
                    flag += 1
                    logs.error('响应文本字符串包含断言失败：未找到字段[%s]' % assert_key)
        return flag

    def equal_assert(self, value, response):
        """
        相等断言模式
        :param value: 预期结果，yaml文件当中的validation关键字下的参数，必须为dict类型
        :param response: 接口的实际返回结果，必须为dict类型
        :return: flag标识，0表示测试通过，非0表示测试不通过
        """
        flag = 0
        # 要求预期和实际都为字典
        if isinstance(value, dict) and isinstance(response, dict):
            res_lst = []
            # 处理实际结果的数据结构：若实际返回是列表，提取与预期key一致的字典
            for res in response:
                if list(value.keys())[0] != res:
                    res_lst.append(res)
            # 删除实际结果中多余的字典（保持与预期结构一致）
            for rl in res_lst:
                del response[rl]

            # 通过 operator.eq 判断实际与预期字典是否完全相等（历史讨论过此模块替代 cmp）
            eq_assert = operator.eq(response, value)
            if eq_assert:
                logs.info(f'相等断言成功：接口的实际结果为：{response}，等于预期结果：{str(value)}')
            else:
                flag += 1
                logs.info(f'相等断言失败：预期结果为：{str(value)}，不等于接口实际返回值：{response}')
        else:
            # 类型错误直接抛异常
            raise TypeError('相等断言失败--类型错误，预期结果和接口的实际响应结果必须为字典类型！')
        return flag

    def not_equal_assert(self, value, response):
        """
        不相等断言模式
        :param value: 预期结果，yaml文件当中的validation关键字下的参数，必须为dict类型
        :param response: 接口的实际返回结果，必须为dict类型
        :return: flag标识，0表示测试通过，非0表示测试不通过
        """
        flag = 0
        if isinstance(value, dict) and isinstance(response, dict):
            res_lst = []
            # 同样处理实际结果结构（适配列表嵌套字典场景）
            for res in response:
                if list(value.keys())[0] != res:
                    res_lst.append(res)
            for rl in res_lst:
                del response[rl]

            # 通过 operator.ne 判断是否不相等
            eq_assert = operator.ne(response, value)
            if eq_assert:
                logs.info(f'不相等断言成功：接口的实际结果为：{response}，不等于预期结果：{str(value)}')
            else:
                flag += 1
                logs.info(f'不相等断言失败：预期结果为：{str(value)}，等于接口实际返回值：{response}')
        else:
            raise TypeError('不相等断言失败--类型错误，预期结果和接口的实际响应结果必须为字典类型！')
        return flag

    def assert_mysql(self, expected_sql):
        """
        数据库断言模式
        :param expected_sql: 预期结果，也就是yaml文件的SQL语句
        :return: 返回flag标识，0表示测试通过，非0表示测试失败
        """
        flag = 0
        conn = ConnectMysql()
        db_value = conn.query(expected_sql)
        # 仅判断查询结果非空（非None），结合历史：query异常返回None，空列表[]会通过
        if db_value is not None:
            logs.info('数据库断言成功')
        else:
            flag += 1
            logs.error('数据库断言失败，请检查数据库是否存在该数据！')
        return flag

    def assert_result(self, expected, response, status_code):
        """
        断言模式，通过all_flag标记
        :param expected: 预期结果，yaml文件当中的validation关键字下的参数
        :param response: 接口的实际返回结果，json格式
        :param status_code: 接口实际返回状态码
        :return:
        """
        all_flag = 0
        try:
            # 遍历 YAML 中的校验配置，分发到不同断言方法
            for yq in expected:
                for key, value in yq.items():
                    if key == 'contains':
                        flag = self.contains_assert(value, response, status_code)
                        all_flag += flag
                    elif key == 'eq':
                        flag = self.equal_assert(value, response)
                        all_flag += flag
                    elif key == 'ne':
                        flag = self.not_equal_assert(value, response)
                        all_flag += flag
                    elif key == 'db':
                        flag = self.assert_mysql(value)
                        all_flag += flag

            # 最终汇总：若 all_flag 为 0 则全部通过，否则失败
            assert all_flag == 0
            logs.info('测试成功！')
        except Exception as e:
            logs.error('测试失败！')
            logs.error(f'异常信息：{e}')
            assert all_flag == 0

    # 截图末尾的 main 调试入口（部分可见）
    # if __name__ == '__main__':
    #     from common.readyaml import get_testcase_yaml
    #     ...

    def assert_mysql(self, expected_sql):
        """
        数据库断言模式
        :param expected_sql: 预期结果，也就是yaml文件的SQL语句
        :return: 返回flag标识，0表示测试通过，非0表示测试失败
        """
        flag = 0
        conn = ConnectMysql()
        db_value = conn.query(expected_sql)
        if db_value is not None:
            logs.info('数据库断言成功')
        else:
            flag = flag + 1
            logs.error('数据库断言失败，请检查数据库是否存在该数据！')
        return flag



