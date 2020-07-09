# 执行test

import ddt
import unittest
import csv
import datetime
import time

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

    """
          1、添加打卡类型：add_type
          2、为除自己之外的其他某位家人创建打卡：add_event
          3、
    """

    # ********* addtype 添加打卡类型 ***********
    # @unittest.skip
    @read_csv_dict("add_type.csv")
    def test_add_type(self, uid,familyId, rewardContent, rewardType, successCount):
        typeName = '文言文翻译' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        print(typeName)


        u = InterfaceCenter.get_user(uid)
        addtype = u.clock_add_type(typeName)
        addtype_status = addtype['status']
        addtype_code = addtype.code
        addtype_message = addtype.message

        # print(code)
        if addtype_code == 200:
            addtype_data = addtype.data
            if addtype_data != None:
                typeId = addtype_data.id    # 【typeID = addtype_id】


                familyusers = u.family_users(familyId)
                familyusers_code = familyusers.code
                familyusers_message = familyusers.message
                user_list = []  # 创建空list存uid
                if familyusers_code == 200:
                    familyusers_data = familyusers.data
                    if familyusers_data != None:

                        for i, item in enumerate(familyusers_data):
                            if item['uid'] != uid:
                                user_list.append(item['uid'])
                        # print('userid数据：',user_list)          #  打印出除该uid外的其他家人的uid
                        executorUid = random.choice(user_list)    # 随机取出uid
                        # print('为该家人创建打卡的uid',executorUid)

                else:
                 print('获取家庭成员列表失败', familyusers_message)

                # ********* addevent创建打卡 ***********
                addevent = u.add_event(typeId,familyId,rewardContent,rewardType,successCount, executorUid)
                addevent_code = addevent.code

                if addevent_code == 200:
                        addevent_data = addevent.data
                        # print('addevent创建打卡成功:', addevent_data)
                        # print('打卡事件ID:', addevent_data.id)
                        eventid = addevent.id


                        # familylist = u.list(familyId)
                        # familylist_code = familylist.code
                        # familylist_message = familylist.message
                        # print(familylist.data)
                        # if familylist_code == 200:
                        #     familylist_data = familylist.data
                        #     if familylist_data != None:
                        #         for i,item  in enumerate(familylist_data):
                        #             if item['eventId'] == eventid:
                        #              familylist.append(item['eventid'])
                        #
                        #             print('111111',familylist)

                        # ********* clockin打卡 ***********
                        eventid = addevent_data.id  # 创建打卡后的ID = 去立即打卡的ID
                        clockuid = InterfaceCenter.get_user(executorUid)  # 获取打卡用户的uid
                        clockin = clockuid.clock_in(eventid)
                        clockin_message = clockin.messaage
                        clockin_code = clockin.code

                        if clockin_code == 200:
                            clockin_data = clockin.data
                            print('clockin打卡成功：',clockin_data)
                        else:
                            print('clockin打卡失败：',clockin)


                else:
                        print('addevent创建打卡失败：',addevent_code)

            else:
                print('addtype添加打卡类型失败:', addtype_code, addtype_message)




if __name__ == '__main__':
    unittest.main()
