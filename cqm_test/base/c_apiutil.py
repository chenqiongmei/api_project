import json
import os
from common.c_debugtalk import DebugTalk
from common.c_read_yaml import ReadYamlData, get_testcase_yaml
from conf.c_operationConfig import OperationConfig
from common.c_sendrequests import SendRequests
from common.c_recordlog import logs
import allure
import re
import json
import jsonpath


class RequestsBase:

    def __init__(self):
        # 实例化 YAML 读取工具（呼应你之前踩坑的“类名加括号”创建对象）
        self.read = ReadYamlData()
        self.conf = OperationConfig()
        self.send = SendRequests()

    def replace_load(self, data):
        """
        yaml文件替换解析所有${}格式的数据
        实现热加载：将用例中的 ${func(arg)} 动态替换为实际运行值
        """
        str_data = data

        # 如果传入的是字典/列表（如接口用例），先转成字符串以便统一正则匹配
        if not isinstance(data, str):
            str_data = json.dumps(data, ensure_ascii=False)

        # 统计字符串中 '${' 的数量，逐个解析（如 ${get_extract_data(token)}）
        for i in range(str_data.count('${')):
            if "${" in str_data and "}" in str_data:
                # 找到 '${' 和 '}' 的索引位置，截取完整占位符
                start_index = str_data.index('${')
                end_index = str_data.index('}', start_index)
                ref_all_params = str_data[start_index:end_index + 1]
                print(ref_all_params)
                # 取出函数名：如 "${get_extract_data(token)}" -> "get_extract_data"
                func_name = ref_all_params[2:ref_all_params.index('(')]
                print(func_name)
                # 取出函数参数：如 "${get_extract_data(token)}" -> "token"
                funcs_params = ref_all_params[ref_all_params.index('(') + 1:ref_all_params.index(')')]
                # 传入替换的参数获取对应值
                print(funcs_params)
                print('yaml文件替换解析前：', str_data)
                # 核心反射调用：从 DebugTalk 类中动态获取函数并执行
                # python反射：对应之前写的 get_extract_data，从 extract.yaml 取真实 token 或 product_id
                extract_data = getattr(DebugTalk(), func_name)(*funcs_params.split(',') if funcs_params else "")
                print(extract_data)
                # 将原占位符替换为实际值（如 '123456'）
                str_data = str_data.replace(ref_all_params, str(extract_data))
                print('yaml文件替换解析后：', str_data)

        # 还原数据：如果原数据是字典，替换后转回字典；否则返回字符串
        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    def specification_yaml(self, case_info):
        """
        规范yaml接口测试数据写法
        :param case_info:list类型，调取case_info[0]
        :return:
        """
        # 判断参数类型，其中params主要指url
        cookie = None
        params_type = ['params', 'data', 'json']

        try:
            base_url = self.conf.get_envi('host')
            url = base_url + case_info['baseInfo']['url']
            # 测试报告右侧输出测试步骤
            allure.attach(url, f'接口地址:{url}')
            api_name = case_info['baseInfo']['api_name']
            allure.attach(api_name, f'接口名称:{api_name}')
            method = case_info['baseInfo']['method']
            allure.attach(method, f'请求方法:{method}')
            header = case_info['baseInfo']['header']
            allure.attach(str(header), f'请求头:{header}', allure.attachment_type.TEXT)

            # baseInfo取自c_login.yaml
            try:
                cookie = self.replace_load(case_info['baseInfo']['header'])
                allure.attach(cookie, f'cookie:{cookie}', allure.attachment_type.TEXT)
            except:
                pass
            # 在c_login.yaml/testCase里遍历取值
            for tc in case_info['testCase']:
                # 返回结果中删除case_name、断言validation、提取extract
                case_name = tc.pop('case_name')
                allure.attach(case_name, f'测试用例名称:{case_name}')
                validation = tc.pop('validation')
                extract = tc.pop('extract', None)
                extract_list = tc.pop('extract_list', None)
                print(tc)
                for key, value in tc.items():
                    print(key, value)
                    if key in params_type:
                        tc[key] = self.replace_load(value)
                # res = self.send.run_main(url=url,data=tc['data'],header=None,method= method)
                # **tc 实现到requests库中动态取data/json/params,如c_login.yaml下是data就传data,json就传json
                res = self.send.run_main(name=api_name, url=url, case_name=case_name, header=header, method=method,
                                         cookies=cookie,
                                         file=None, **tc)
                res.text = res.text
                allure.attach(res.text, f'接口响应信息:{res.text}', allure.attachment_type.TEXT)
                allure.attach(str(res.status_code), f'状态码:{res.status_code}', allure.attachment_type.TEXT)

                print(res.text)
                if extract is not None:
                    self.extract_data(extract, res.text)
                if extract_list is not None:
                    self.extract_data_list(extract_list, res.text)
        except Exception as e:
            logs.error()
            raise e  # 返回异常体现在测试报告中

    # def extract_list_data(self,testcase_extract_list, response):  # .search改成.findall

    def extract_data(self, testcase_extract, response):
        """
        提取接口返回值，支持正则表达式提取器及json提取器
        :param testcase_extract:yaml文件中extract的值
        :param response:接口实际返回值
        :return:
        """
        # 定义正则模式列表，用于匹配提取表达式（注：前两项重复，且为字符串形式）
        # 注：参数名 tesecase_extract 疑似 testcase_extract 笔误，pattenr_lst 疑似 pattern_lst 笔误
        pattern_lst = ['(.+?)', '(.+?)', r'(\d+)', r'(\d*)']
        try:
            for key, value in testcase_extract.items():
                print(key, value)
                # 遍历预设的正则模式字符串
                for pat in pattern_lst:
                    # 判断模式字符串是否包含在提取表达式中（字符串包含判断，非正则匹配）
                    if pat in value:
                        # 在响应文本中搜索匹配提取表达式
                        ext_list = re.search(value, response)
                        # 若当前模式为数字匹配，则尝试转为int
                        if pat in [r'(\d+)', r'(\d*)']:
                            # 将匹配到的第一组转为整数并存入字典（注：若匹配空串可能报错）
                            extract_data = {key: int(ext_list.group(1))}
                        else:
                            # 否则存为字符串（注：ext_list若为None会报AttributeError）
                            extract_data = {key: ext_list.group(1)}
                            logs.info(f'正则提取到的参数：{extract_data}')
                            self.read.write_yaml_data(extract_data)
                        # 打印提取结果（注：函数无return，仅打印；且内层未break会覆盖）
                        print(extract_data)
                # 遍历预设的json提取器字符串处理，判断是否为jsonpath表达式（以"$"开头）
                if "$" in value:
                    # 解析响应为json并使用jsonpath提取（取第一个匹配结果）
                    ext_json = jsonpath.jsonpath(json.loads(response), value)[0]
                    # 若提取到结果
                    if ext_json:
                        extract_data = {key: ext_json}
                    else:
                        # 未提取到时的默认提示
                        extract_data = {key: '未提取到数据，该接口返回值为空或者json提取表达式有误！'}
                    # 打印json提取日志
                    logs.info(f'json提取到的参数: {extract_data}')
                    # 将提取结果写入yaml
                    self.read.write_yaml_data(extract_data)
        except:
            logs.error('接口返回值提取异常，请检查yaml文件的extract表达式是否正确！')

    def extract_data_list(self, testcase_extract_list, response):
        """
        提取多个参数，支持正则表达式和json提取，提取结果以列表形式返回
        :param testcase_extract_list: yaml文件中的extract_list信息
        :param response: 接口的实际返回值,str类型
        :return:
        """
        try:
            for key, value in testcase_extract_list.items():
                if "(.+?)" in value or "(.*?)" in value:
                    ext_list = re.findall(value, response, re.S)
                    if ext_list:
                        extract_date = {key: ext_list}
                        logs.info('正则提取到的参数：%s' % extract_date)
                        self.read.write_yaml_data(extract_date)
                if "$" in value:
                    # 增加提取判断，有些返回结果为空提取不到，给一个默认值
                    ext_json = jsonpath.jsonpath(json.loads(response), value)
                    if ext_json:
                        extract_date = {key: ext_json}
                    else:
                        extract_date = {key: "未提取到数据，该接口返回结果可能为空"}
                    logs.info('json提取到参数：%s' % extract_date)
                    self.read.write_yaml_data(extract_date)
        except:
            logs.error('接口返回值提取异常，请检查yaml文件extract_list表达式是否正确！')


if __name__ == '__main__':
    YAML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'testcase', 'Login', 'c_login.yaml')
    req = RequestsBase()
    data = get_testcase_yaml(YAML_PATH)[0]
    print(data)
    print(req.specification_yaml(data))

# if __name__ == '__main__':
#     YAML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'testcase', 'Login', 'c_login.yaml')
#     data = get_testcase_yaml(YAML_PATH)[0]
#     # data = get_testcase_yaml('c_login.yaml')[0]
#     print(data)
#     base = BaseRequests()
#     res = base.replace_load(data)
#     print(res)
