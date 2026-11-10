from common.c_recordlog import logs
from conf.c_operationConfig import OperationConfig
import pymysql

# 实例化配置读取类（对应你上一轮的 get_mysql_conf 方法）
conf = OperationConfig()

class ConnectMysql:
    """连接读取MySQL数据库的数据"""

    def __init__(self):
        # 从 config.ini 的 [MYSQL/MASQL] 区块读取配置，组装连接参数
        # 注意：port 需转为 int，其余为字符串
        mysql_conf = {
            'host': conf.get_mysql_conf('host'),
            'port': int(conf.get_mysql_conf('port')),
            'user': conf.get_mysql_conf('username'),
            'password': conf.get_mysql_conf('password'),
            'database': conf.get_mysql_conf('database')
        }

        try:
            # **mysql_conf 解包传参，指定 utf8 编码
            self.conn = pymysql.connect(**mysql_conf, charset='utf8')
            # 使用 DictCursor：查询结果为字典格式（字段名作为 key），便于后续接口断言比对
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logs.info("成功连接到MySQL数据库\nhost: {host}\nport: {port}\ndb: {database}".format(**mysql_conf))
        except Exception as e:
            logs.error(e)

    def close(self):
        """关闭游标与数据库连接，释放资源"""
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()

    def query(self, sql):
        """查询数据"""
        try:
            self.cursor.execute(sql)
            # 查询操作通常无需 commit，此处保留可能是为了兼容某些特殊场景（如即时生效的写入后查）
            self.conn.commit()
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            logs.error(e)
        finally:
            # 每次查询后自动关闭连接（短连接模式）
            # 注意：若高频查询，建议将 close 移出，由外部调用方统一管理生命周期
            self.close()

    def insert(self):
        """插入数据"""

    def update(self):
        """修改数据"""

    def delete(self):
        """删除数据"""


if __name__ == '__main__':
    # 本地调试入口
    conn = ConnectMysql()
    sql = 'select * from tb_vehicle_info limit 5'
    print(conn.query(sql))

