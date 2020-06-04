import ddt
import unittest

import random
from common.ddt_csv_reader import read_csv_dict
import json
from interface.backstage import Backstage
from interface.Backstage_ad import Backstage_ad

from interface.result_sql import Result_sql
from common import read_csv_dict
from model.factory import InterfaceCenter
user_file='yyx.json'
InterfaceCenter.set_user_file(user_file)

@ddt.ddt
class test_Topic(unittest.TestCase):
    #@unittest.skip
    @read_csv_dict("test_topic1.csv")
    def test_topic(self,uid,name,password,title,subtitle, content,thumbnail,background,sort,
                         status,type,options):

        """
        创建话题流程
        1.登录后台
        2.获取list接口，前端展示得接口
        3.创建话题
        4.获取list接口
        5.获取前端展示得接口
        6.获取话题详情页面
        7，修改话题详情
        """

        user=Backstage()
        #登录后台获取token
        login=user.bs_login(name,password)
        login_code = login['code']
        login_message = login['message']
        if login_code == 200 and login_message=="Success":
            token = login['data']['token']
            creat=Backstage_ad()
            #新建话题
            creat_cate=creat.bs_create_cate(token,title,subtitle,content,thumbnail,background,sort,
                         status,type,options)
            creat_code=creat_cate.code
            creat_message=creat_cate.message
            if creat_code == 200:
                id=creat_cate.data.id
                print(id)
                #查看话题列表
                cate_list=creat.bs_cate_list(token,type,)
                cate_list_code=cate_list.code

                cate_list_message=cate_list.message
                if cate_list_code == 200:
                    cate_list_data=cate_list.data.list
                    if cate_list != None:
                        for i, item in enumerate(cate_list_data):
                            cate_id=int(item['id'])
                            print(11111)
                            print(int(cate_id) is id)
                            if cate_id ==id:
                                print("新建话题成功,后台列表增加数据成功")
                                return
                else:
                    print('cate_list_message' + cate_list_message)

            else:
                print('creat_message' + creat_message)
            u = InterfaceCenter.get_user(uid)
            type = 0
            topic = u.home_topic(type)
            topic_code = topic.code
            topic_message=topic.message
            if topic_code == 200:
                topic_data=topic.data
                print(topic_data)
                if topic_data != None:
                    for i,item in enumerate(topic_data):
                        if id==item['id']:
                            print('home_topic接口增加了话题数据')
            else:
                print('topic_message',topic_message)
        else:
            print('message' , login_message)




if __name__=='__main__':
    unittest.main()