import ddt
import unittest

import random
from common.ddt_csv_reader import read_csv_dict
import json
from interface.contents import Content
from interface.result_sql import Result_sql
from common import read_csv_dict
from model.factory import InterfaceCenter
user_file='yyx.json'
InterfaceCenter.set_user_file(user_file)

@ddt.ddt
class snow_Yyx(unittest.TestCase):
    #@unittest.skip
    @read_csv_dict("body.csv")
    def testhometopic(self,uid,type):

        """
        校验home_topic接口是否请求成功，
        """
        u = InterfaceCenter.get_user(uid)
        a = u.home_topic(type)

        staus = a['status']
        code = a.code
        #print(code)
        if code == '401':
            print('参数解析错误')
        elif code == '500':
            print('服务端错误')
        elif code =='101':
            print('用户信息错误')
        elif code =='404':
            print("页面未找到")
        elif code =='200':
            data=a.data
            print('请求接口成功'+ data)



if __name__=='__main__':
    unittest.main()