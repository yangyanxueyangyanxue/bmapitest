import pymysql
from common.log import logger
from common.db_conf import MYSQL_ALL_DB
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text, create_engine, Table, MetaData

_connections={}
Base=declarative_base()
#工厂模式，数据库链接实例创建工厂

def connect(db_name):
    assert db_name in MYSQL_ALL_DB,'db not found'
    #单例模式，对于每个数据库只创建一个连接实例,
    # #把表映射为一个类  这样在程序中才可以使用
    #程序是不能直接操作数据库的,程序只能操作自己的类,可以看下orm的知识
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
        logger.info('create mysql connection ok :%s' % db_name)
    return None

class TableModel:
    def __init__(self,session,TableClass):
        self.seesion=session
        self.TableClass=TableClass

    def selfect(self,where_list):
        where_text,is_all=self._where_text(where_list)
        self.session.commit()
        return self._query(where_text,is_all)

    def update(self,where_list,set_dict):
        where_text,is_all=self._where_text(where_list)
        self.seeion.commit()
        return self._query(where_text,is_all)

    def update(self,where_list,set_dict):
        where_text, is_all=self._where_text(where_list)
        result=self._quert(where_text,is_all)
        for res in result:
            for key,value in set_dict.items():
                setattr(res,key,value)
            self.session.commit()

    def delete(self,where_list):
        where_text,is_all=self._where_test(where_list)
        result=self._query(where_text,is_all)
        for res in result:
            self.session.delete(res)
        self.session.commit()

    def insert(self,data):
        self.session.add(self.TableClass(**data))
        self.session.commit()

    def where_text(self,where_list):
        if not where_list:
            return None,True
        if where_list[0] =="and":
            where_text=self._and(where_list[1:])
        elif where_list[0]=="or":
            where_text=self._or(where_list[1:])
        else:
            where_text=self._and(where_list)
        return where_text,False

    def _query(self,where_text,is_all):
        # 很坑, 被sqlalchemy的text组装过的where_text, 无法判断其bool值
        if is_all:
            return self.session.query(self.TableClass).all()
        return self.session.query(self.TableClass).filter(where_text).all()

    def _and(self,where):
        return text("and".join(where))

    def _or(self,where):
        return text("or".join(where))














