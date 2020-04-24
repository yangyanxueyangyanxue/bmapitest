#数据库的相关信息（host,username,password等，统一在db_conf中
from common import mysql_db
import time

def select_username_by_uid_and_phone(uid,phone):
    #创建数据库实例，数据库命等相关信息在mysql_conf.py中配置
    db=mysql_db.connect("local")
    #创建数据表实例，表为数据库中一张存在的表
    table_users=db.get_table("users")
    #where 子句
    #支持符号：<,<=,>,>=,=,!=
    #默认为and连接
    where_list=[
        "uid={}".fomat(uid),

    ]
    #支持or连接，以下为or 连接示例
    #列表 第0位添加"and".或"or"
    #where =[
    # "or",
    # "uid={}".foemat(uid),
    # "phone_number={}".format(phone),
    # "id<10"
    # ]
    result =table_users.selectt(where_list)
    return result

def select_member_info(uid):
    db = mysql_db.connect("member")
    member_info = db.get_table("bm_member")
    where_list = [
        "uid = '{}'".format(uid)
    ]
    return member_info.select(where_list)

def insert_member_info(uid):
    db = mysql_db.connect("bbmmapptest")
    member_info = db.get_table("bm_member")
    where_list = [
        "uid = '{}'".format(uid)
    ]
    return member_info.insert(where_list)

def update_member_info(uid):
    db = mysql_db.connect("bbmmapptest")
    member_info = db.get_table("bm_member")
    where_list = [
        "uid = '{}'".format(uid)
    ]
    return member_info.update(where_list)

def delete_by_uid_and_phone(uid, phone):
    db = mysql_db.connect("bbmmapptest")
    table_users = db.get_table("users")
    where_list = [
        "uid = {}".format(uid),
        "phone_number = {}".format(phone)
    ]
    table_users.delete(where_list)