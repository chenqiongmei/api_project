import pymysql
import redis
from rediscluster import RedisCluster

from common.recordlog import logs
from conf.operationConfig import OperationConfig

conf = OperationConfig()


class MysqlDbClient:
    """
    操作MySQL数据库
    """

    def __init__(self):
        self.__mysql_conf = {
            'host': conf.get_section_mysql('host'),
            'port': int(conf.get_section_mysql('port')),
            'user': conf.get_section_mysql('user'),
            'password': conf.get_section_mysql('password'),
            'database': conf.get_section_mysql('database')
        }

        self.conn = pymysql.connect(**self.__mysql_conf)
        # cursor=pymysql.cursors.DictCursor 将结果返回字典类型
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        try:
            # 关闭连接
            self.conn.close()
            # 关闭游标
            self.cur.close()
        except AttributeError as error:
            logs.error(error)

    def query(self, sql, query_type='all'):
        """
        查询数据库
        :param sql: 查询语句
        :param query_type: 查询类型，默认查询全部数据，不为all则查询单条数据
        :return:
        """
        try:
            self.cur.execute(sql)
            if query_type == 'all':
                data = self.cur.fetchall()
            else:
                data = self.cur.fetchone()
            return data
        except AttributeError as error:
            logs.error(f"数据库查询失败，失败原因：{error}")

    def execute(self, sql):
        """
        MySQL数据库增删改操作
        :param sql: 增删改的SQL语句
        :return:
        """
        try:
            rows = self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
            return rows
        except AttributeError as error:
            logs.error(f"数据库操作失败，失败原因：{error}")
            # 如果事务异常，则回滚数据
            self.conn.rollback()
            raise


class RedisClient:
    """
    从Redis中读取、设置相关数据
    """

    def __init__(self):
        self.__redis_conf = {
            'host': conf.get_section_redis('host'),
            'port': int(conf.get_section_redis('port')),
            'username': conf.get_section_redis('username'),
            'password': conf.get_section_redis('password'),
            'db': conf.get_section_redis('db')
        }
        redis_nodes_str = conf.get_section_redis('startup_nodes')
        self.nodes_list = []
        if redis_nodes_str:
            nodes_str_list = redis_nodes_str.split(',')
            for node_str in nodes_str_list:
                host, port = node_str.split(':')
                node_data = {'host': host, 'port': port}
                self.nodes_list.append(node_data)

            # startup_nodes：集群的格式[{'host':'host','port':'port'},{'host2':'host2','port2':'port2'},{},....]
            self.redis_cluster = RedisCluster(startup_nodes=self.nodes_list)
            logs.info(f'连接到Redis集群服务，host：{redis_nodes_str}')

        elif self.__redis_conf['host'] and self.__redis_conf['port']:
            try:
                logs.info(f'连接到Redis服务器：ip：{self.__redis_conf["host"]}')
                pool = redis.ConnectionPool(**self.__redis_conf)
                self.redis_cluster = redis.Redis(connection_pool=pool)
            except Exception as e:
                logs.error(f'redis连接失败，{e}')

    @classmethod
    def redis_except(cls, e):
        if "MOVED" in str(e):
            logs.error(f'请检查Redis是否使用了集群模式或者主从复制的情况，数据被迁移到了另外一个Redis实例上：{e}')
        else:
            logs.error(f'Redis Error：{e}')

    def get(self, key):
        """
        获取Redis里面的数据
        :param key: Redis里面的键
        :return:
        """
        try:
            value = self.redis_cluster.get(key)
            if isinstance(value, bytes):
                return value.decode('utf-8')
            return value
        except Exception as e:
            self.redis_except(e)

    def set(self, key, value, ex=None):
        """
        设置Redis的值
        :param key: Redis键
        :param value: 需要设置的内容
        :param ex: 过期时间，单秒（s)
        :return:
        """
        try:
            return self.redis_cluster.set(name=key, value=value, ex=ex)
        except Exception as e:
            logs.redis_except(e)


if __name__ == '__main__':
    redis_con = RedisClient()
    key = "sdyqfk:vehicle:enter:lock"
    res = redis_con.get(key)
    print(res)
