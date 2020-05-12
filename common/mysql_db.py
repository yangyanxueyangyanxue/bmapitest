import pymysql
from common.log import logger
from common.db_conf import MYSQL_ALL_DB
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text, create_engine, Table, MetaData

_connections = {}
Base = declarative_base()

# 工厂模式, 数据库连接实例创建工厂


def connect(db_name):
    assert db_name in MYSQL_ALL_DB, 'db not found'
    # 单例模式, 对于每个数据库只创建一个连接实例
    if db_name in _connections:
        return _connections[db_name]
    try:
        db = MYSQL_ALL_DB[db_name]
        engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(
            db.get("user"), db.get("password"), db.get(
                "host"), db.get("port", 3306), db.get("database")
        ), encoding="utf-8")
        _connections[db_name] = DBModel(engine)
    except Exception as e:
        logger.error(e)
    else:
        logger.info('create mysql connection ok: %s' % db_name)
        return _connections[db_name]
    return None


class DBModel:
    tables = {}

    def __init__(self, engine):
        self.session = Session(engine)
        self.metadata = MetaData(engine)

    def select_cmd(self, cmd):
        return self.session.execute(cmd)

    def execute_cmd(self, cmd):
        self.session.execute(cmd)
        self.session.commit()

    def get_table(self, table_name):
        # 单例模式, 对于每个数据表只创建一个映射类
        if table_name in DBModel.tables:
            return TableModel(self.session, DBModel.tables[table_name])
        try:
            table = Table(table_name, self.metadata, autoload=True)
            # 动态生成 orm 表结构类
            TableClass = type(table_name, (Base, ), {"__table__": table})
            DBModel.tables[table_name] = TableClass
        except Exception as e:
            logger.error(e)
        else:
            logger.info('create mysql table ok: %s' % table_name)
            return TableModel(self.session, TableClass)
        return None


class TableModel:
    def __init__(self, session, TableClass):
        self.session = session
        self.TableClass = TableClass

    def select(self, where_list):
        where_text, is_all = self._where_text(where_list)
        self.session.commit()
        return self._query(where_text, is_all)

    def update(self, where_list, set_dict):
        where_text, is_all = self._where_text(where_list)
        result = self._query(where_text, is_all)
        for res in result:
            for key, value in set_dict.items():
                setattr(res, key, value)
        self.session.commit()

    def delete(self, where_list):
        where_text, is_all = self._where_text(where_list)
        result = self._query(where_text, is_all)
        for res in result:
            self.session.delete(res)
        self.session.commit()

    def insert(self, data):
        self.session.add(self.TableClass(**data))
        self.session.commit()

    def _where_text(self, where_list):
        if not where_list:
            return None, True
        if where_list[0] == "and":
            where_text = self._and(where_list[1:])
        elif where_list[0] == "or":
            where_text = self._or(where_list[1:])
        else:
            where_text = self._and(where_list)
        return where_text, False

    def _query(self, where_text, is_all):
        # 很坑, 被sqlalchemy的text组装过的where_text, 无法判断其bool值
        if is_all:
            return self.session.query(self.TableClass).all()
        return self.session.query(self.TableClass).filter(where_text).all()

    def _and(self, where):
        return text(" and ".join(where))

    def _or(self, where):
        return text(" or ".join(where))
