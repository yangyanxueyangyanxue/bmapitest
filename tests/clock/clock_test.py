# 执行test

import ddt
import unittest
import csv

import random
from common.ddt_csv_reader import read_csv_dict
import json
from interface.clock import Clock
from interface.result_sql import Result_sql
from common import read_csv_dict
from model.factory import InterfaceCenter

user_file = '10213.json'
InterfaceCenter.set_user_file(user_file)


@ddt.ddt
class test_Hxl(unittest.TestCase):
    # @unittest.skip

    """
       1、添加打卡类型：add_type
       2、为该家人创建打卡：add_event
       3、
    """

    @read_csv_dict("add_type.csv")
    # 添加打卡类型
    def test_add_type(self, uid, typeName,familyId, rewardContent, rewardType, successCount, executorUid):
        """
        校验add_type接口是否请求成功
        """
        u = InterfaceCenter.get_user(uid)
        addtype = u.add_type(typeName)

        addtype_status = addtype['status']
        addtype_code = addtype.code
        addtype_message = addtype.message
        # print(code)
        if addtype_code == 200:
            addtype_data = addtype.data
            if addtype_data != None:
                typeId = addtype_data.id
                familylist = u.get_family()
                familylist_data = familylist.data
                # print(familylist_data)


                addevent = u.add_event(typeId,familyId,rewardContent,rewardType,successCount, executorUid)
                print(addevent)
                addevent_message = addevent.message
                addevent_code = addevent.code

                if addevent_code == 200:
                    addevent_data = addevent.data
                    # print('请求接口成功:', addevent_data)
                    # print(addevent_data[1])

                    # if addevent_data != None:
                    for i, item in enumerate(addevent_data):

                        if familyId == item['familyId']:
                            users = item['users']
                            users1 = random.randint(len(users))  # 随机取出list里的小于下标长度的一个字典
                            cover_uid = users[users1]["uid"]  # 随机取出字典的元素
                            print(users1)



                            eventId = random.randint(len(users))

                            print('添加打卡事件   ',eventId)
                else:
                    print('addevent失败：',addevent_code,addevent_message)




        else:
            print('返回失败:', addtype_code, addtype_message)


    # @read_csv_dict("add_event.csv")
    # # 创建打卡
    # def test_add_event(self,uid,typeId,familyId,rewardContent,rewardType,successCount,executorUid):
    #     """
    #     校验add_event接口是否请求成功
    #     """
    #     u = InterfaceCenter.get_user(uid)
    #     a = u.add_event(typeId,familyId,rewardContent,rewardType,successCount,executorUid)
    #
    #     status = a['status']
    #     code = a.code
    #     message = a.message
    #     # print(code)
    #     if code == 200:
    #         data = a.data
    #         print('请求接口成功:', data)
    #
    #     else:
    #         print('返回失败:', code, message)



    # @read_csv_dict("clock_in.csv")
    # 立即打卡
    # def test_clock_in(self,uid,eventId):
    #     """
    #     校验clock_in接口是否请求成功
    #     """
    #     u = InterfaceCenter.get_user(uid)
    #     a = u.clock_in(eventId)
    #
    #     status = a['status']
    #     code = a.code
    #     message = a.message
    #     #print(code)
    #     if code == 200:
    #         data = a.data
    #         print('请求接口成功:',data)
    #
    #     else:
    #         print('返回失败:',code,message)


if __name__ == '__main__':
    unittest.main()
