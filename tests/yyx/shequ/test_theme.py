import ddt
import unittest

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
    def test_theme(self,uid,type,title,content,syncAlbum):
        """
        放到话题里的动态 1.打开话题列表（判断下是否有，没有的就走创建，有的话随便取值一个）2我要发布（自己展示，别人不展示）3后台审核4勾选最新和推荐，可以展示出了
        先请求home_topic 话题列表，找到对应话题，进入话题详情页面 them 最新和推荐 ，我要发布 family_list,发布save,file/upload 然后看them接口是否有新数据，传个别的token，看别人的详情不展示，登录后台，作品管理，审核
        audit/list接口的新数据--content/conent接口是动态详情，推荐到首页和最新，operate接口操作成功，查看他人的动态详情
        """

        u = InterfaceCenter.get_user(uid)
        topic = u.home_topic(type)
        topic_code = topic.code
        topic_message = topic.message
        if topic_code == 200:
            topic_data = topic.data
            print(topic_data)
            if topic_data != None:
                type = 1
                cateId = topic_data[0]['id']
                page = 1
                cateIds = []
                cateIds.append(cateId)
                Comments_save = u.Comments_save(cateIds, title, content, syncAlbum)
                Comments_save_code = Comments_save.code
                Comments_save_message = Comments_save.message
                if Comments_save_code == 200:
                    Comments_save_data = Comments_save.data
                    if Comments_save_data != None:
                        save_data_id = Comments_save.data.id
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
                        else:
                            print('them_message', them_message)
                            # 后台审核动态，然后查看他人首页是否有这个动态
                else:
                    print('Comments_save_message', Comments_save_message)

        else:
            print('topic_message', topic_message)


if __name__=='__main__':
    unittest.main()