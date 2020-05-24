# 数据库的相关信息（host，username，password等）统一放到 db_conf 中
from common import mysql_db
import time
from common.mysql_db import TableModel


def select_username_by_uid_and_phone(uid,phone):
    # 创建数据库实例, 数据库名等相关信息在 mysql_conf.py 中配置
    db = mysql_db.connect("bbmmapptest")

    #创建数据表实例, 表为数据库中一张存在的表
    table_users = db.get_table("bm_member")

    # where 子句
    # 支持符号: <, <=, >, >=, =, !=
    # 默认为 and 连接
    where_list = [
        "uid = {}".format(uid),
        "phone = {}".format(phone)

    ]
    # 支持 or 连接, 以下为 or 连接示例
    # 列表 第 0 位 添加"and" 或 "or"
    # where = [
    #     "or",
    #     "uid = {}".format(uid),
    #     "phone_number = {}".format(phone),
    #     "id < 10"
    # ]

    result = table_users.select(where_list)

    return result


def update_username_by_uid_and_phone(uid, phone, set_dict):
    db = mysql_db.connect("local")
    table_users = db.get_table("users")
    where_list = [
        "uid = {}".format(uid),
        "phone_number = {}".format(phone)
    ]
    table_users.update(where_list, set_dict)


def delete_by_uid_and_phone(uid, phone):
    db = mysql_db.connect("local")
    table_users = db.get_table("users")
    where_list = [
        "uid = {}".format(uid),
        "phone_number = {}".format(phone)
    ]
    table_users.delete(where_list)


def insert_into_users(insert_data):
    db = mysql_db.connect("local")
    table_users = db.get_table("users")
    table_users.insert(insert_data)


def select_video_process_info_by_pid(process_id):
    db = mysql_db.connect("boss")
    video_process_info = db.get_table("video_process_info")
    where_list = [
        "pid = '{}'".format(process_id)
    ]
    return video_process_info.select(where_list)


def update_video_process_info_by_pid(process_id, set_dict):
    db = mysql_db.connect("boss")
    video_process_info = db.get_table("video_process_info")
    where_list = [
        "pid = '{}'".format(process_id)
    ]
    video_process_info.update(where_list, set_dict)


def insert_video_process_info(insert_data):
    db = mysql_db.connect("boss")
    video_process_info = db.get_table("video_process_info")
    insert_data.update({
        "create_time": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    video_process_info.insert(insert_data)


def select_video_user_info_by_status(status):
    db = mysql_db.connect("boss")
    video_user_info = db.get_table("video_user_info")
    where_list = [
        "status = {}".format(status)
    ]
    return video_user_info.select(where_list)


def update_video_user_info_by_uid(user_id, set_dict):
    db = mysql_db.connect("boss")
    video_user_info = db.get_table("video_user_info")
    where_list = [
        "uid = '{}'".format(user_id)
    ]
    video_user_info.update(where_list, set_dict)


def select_video_info(process_id, video_id):
    db = mysql_db.connect("boss")
    video_info = db.get_table("video_info")
    where_list = [
        "pid = '{}'".format(process_id),
        "vid = '{}'".format(video_id)
    ]
    if not video_id:
        where_list.pop()
    return video_info.select(where_list)


def insert_video_info(insert_data):
    db = mysql_db.connect("boss")
    video_info = db.get_table("video_info")
    insert_data.update({
        "create_time": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    video_info.insert(insert_data)


def update_video_info(video_id, set_dict):
    db = mysql_db.connect("boss")
    video_info = db.get_table("video_info")
    where_list = [
        "vid = '{}'".format(video_id)
    ]
    video_info.update(where_list, set_dict)


def select_im_stress_info(stress_id):
    db = mysql_db.connect("bbmmapptest")
    im_stress_info = db.get_table("")
    where_list = [
        "stress_id = '{}'".format(stress_id)
    ]
    return im_stress_info.select(where_list)


def insert_im_stress_info(insert_data):
    db = mysql_db.connect("boss")
    im_stress_info = db.get_table("im_stress_info")
    insert_data.update({
        "create_time": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    im_stress_info.insert(insert_data)


def update_im_stress_info(stress_id, set_dict):
    db = mysql_db.connect("boss")
    im_stress_info = db.get_table("im_stress_info")
    where_list = [
        "stress_id = '{}'".format(stress_id)
    ]
    im_stress_info.update(where_list, set_dict)


def select_im_msg(msg_type):
    db = mysql_db.connect("boss")
    im = db.get_table("im_msg")
    where_list = [
        "msg_type = '{}'".format(msg_type)
    ]
    if not msg_type:
        where_list = []
    return im.select(where_list)
