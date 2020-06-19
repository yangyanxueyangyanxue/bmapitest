import ddt
import unittest
import sys
import random

import json
from interface.backstage import Backstage
from interface.Backstage_ad import Backstage_ad
from interface.contents import Content
from interface.result_sql import Result_sql
from common import read_csv_dict
from model.factory import InterfaceCenter
user_file='yyx.json'
InterfaceCenter.set_user_file(user_file)

@ddt.ddt
class Theme(unittest.TestCase):
    # @unittest.skip
    @read_csv_dict("test_them.csv")
    def test_theme_type(self,uid,name,password,type,title,content,status,remark,recomHome,recomCate,homeStartTime,cateStartTime):
        """
        放到话题里的动态
        1.打开话题列表（判断下是否有，没有的就走创建，有的话随便取值一个）
        2我要发布（自己展示，别人不展示）
        3后台审核4勾选最新和推荐，可以展示出了
        4先请求home_topic 话题列表，找到对应话题，进入话题详情页面 them 最新和推荐
        5我要发布 family_list,发布save,file/upload
        6然后看them接口是否有新数据，传个别的token，看别人的详情不展示，登录后台，作品管理，审核
        7audit/list接口的新数据--content/conent接口是动态详情，推荐到首页和最新，operate接口操作成功，查看他人的动态详情
        """
        # caseld= sys._getframe().f_code.co_name #当前类名称（测试用例名称）

        u = InterfaceCenter.get_user(uid)

        topic = u.home_topic(type)
        topic_code = topic.code
        topic_message = topic.message
        if topic_code == 200:
            topic_data = topic.data
            print(topic_data)
            if topic_data != None:
                type = 1
                cateId = topic_data[0]['id']  #取出第一个话题 ，或者可以随机取一个话题
                page = 1
                cateIds = []
                cateIds.append(cateId)

                Comments_save = u.Comments_save(cateIds,title,content)
                Comments_save_code = Comments_save.code
                Comments_save_message = Comments_save.message
                if Comments_save_code == 200:
                    Comments_save_data = Comments_save.data
                    if Comments_save_data != None:
                        save_data_id = Comments_save.data.id
                        #发布成功后，后台审核 1.登录后台获取token。2查看作品审核列表3.找到对应得审核，放到首页和推荐

                        user = Backstage()
                        login = user.bs_login(name, password)
                        login_code = login['code']
                        login_message = login['message']
                        if login_code == 200 and login_message == "Success":
                            token = login['data']['token']
                            ad= Backstage_ad()
                            audit_list=ad.bs_audit_list(token)
                            audit_list_code=audit_list.code
                            audit_list_message=audit_list.message
                            if audit_list_code == 200 and audit_list_message == "Success":

                                audit_list=audit_list.data.list
                                if audit_list != None:

                                    for i,item in enumerate(audit_list):

                                        contentId=int(item['contentId'])
                                        print(111,contentId)
                                        if save_data_id==contentId:

                                            #后台作品审核，上到首页和推荐话题
                                            operate=ad.bs_audit_operate(token,contentId,status,recomCate,recomHome,remark,homeStartTime,cateStartTime)
                                            operate_code=operate.code
                                            operate_message=operate.message
                                            if operate_code==200:
                                                print("后台作品审核通过，并且推荐到首页和推荐到话题")
                                                type=1 #话题推荐页面
                                                them = u.comments_theme(type, cateId, page)
                                                them_code = them.code
                                                them_message = them.message
                                                if them_code == 200:
                                                    them_data = them.data
                                                    if them_data != None:
                                                        them_data_cate = them.data.cate
                                                        if them.data.cate != None:
                                                            them_data_cate_list = them.data.cate.list
                                                            if them_data_cate_list != None:
                                                                for i, item in enumerate(them_data_cate_list):
                                                                    self.assertEqual(int(save_data_id), int(item['id']))
                                                                    print("测试通过，话题推荐页面展示出数据")
                                                # topic = u.home_topic(type) #首页推荐动态,page默认传得0，其实数据又可能在下面得页数。需要校验
                                                # topic_code = topic.code
                                                # topic_message = topic.message
                                                # if topic_code == 200:
                                                #     topic_data = topic.data
                                                #
                                                #     print(topic_data,111)
                                                #     for i, item in enumerate(topic_data):
                                                #         self.assertEqual(int(save_data_id), int(item['id']))
                                                #         print("测试通过，首页推荐页面展示出数据")

                                                else:
                                                    print('them_message', them_message)
                                            else:

                                                print(operate_message)
                            else:
                                print(audit_list_code,audit_list_message)
                else:
                    print('Comments_save_message', Comments_save_message)

        else:
            print('topic_message', topic_message)









if __name__=='__main__':
    unittest.main()