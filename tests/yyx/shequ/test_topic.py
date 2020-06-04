import ddt
import unittest

import random
from common.ddt_csv_reader import read_csv_dict
import json
from interface.community import Community
from interface.backstage import Backstage
from interface.backstage import Backstage_ad

from interface.result_sql import Result_sql
from common import read_csv_dict
from model.factory import InterfaceCenter
user_file='yyx.json'
InterfaceCenter.set_user_file(user_file)

@ddt.ddt
class test_Topic(unittest.TestCase):
    #@unittest.skip
    @read_csv_dict("test_topic1.csv")
    def test_topic(self,name,password):

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
        login=user.bs_login(name,password)
        
        print(login)
        code = login['code']
        message=login['message']
        #print(code)
        if code == '200':
            token = login['data']['token']
            print(token)
        elif code == '500':

            print(message)
        elif code =='400':
            print('message')



if __name__=='__main__':
    unittest.main()