import ddt
import unittest
import time
import random
from common.ddt_csv_reader import read_csv_dict
import json
from interface.contents import Content
from interface.result_sql import Result_sql
# from common import read_csv_dict
from model.factory import InterfaceCenter

user_file = 'yyx.json'
InterfaceCenter.set_user_file(user_file)


@ddt.ddt
class Creatbook(unittest.TestCase):
    # @unittest.skip
    @read_csv_dict("creaphotograph.csv")
    def test_creaphotograph(self,uid,familyId):

        """
        制作影集
        1.打开影集，请求影集效果列表接口  首页-+—选择模板--制作影集
        2.选择影集模板
        3.发布影集
        4，影集详情页面
        5.影集分享
        """
        u = InterfaceCenter.get_user(uid)
        template=u.photograph_template()
        template_code=template.code

        if template_code==200:
            template_data=template.data
            if template_data != None:

                templateId=template.data[0]['id']
                title=template.data[0]['title']
        familyIds=[]
        familyIds.append(int(familyId))
        print(familyIds)
        pic_list = u.fm_pic_list(familyId)
        pic_list_code=pic_list.code
        pic1=[]
        pic2=[]
        id=1 #网络图片
        if pic_list_code == 200:
            total = pic_list.data.total
            if total != 0:
                pic_id1 = pic_list.data.list[0]['pic_id']
                pic_id2=pic_list.data.list[1]['pic_id']
                pic1.append(int(pic_id1))
                pic1.append(id)
                pic2.append(int(pic_id2))
                pic2.append(id)
            pics=[pic1,pic2]

            print(pics)
            photograph_save=u.photograph_save(familyIds,title,templateId,id)
            photograph_save_code=photograph_save.code
            if photograph_save_code==200:
                photograph_save_id=photograph_save.data.id
                print(photograph_save_id)
                photograph_effect=u.photograph_effect()
            else:
                photograph_effect = u.memory_album_list(familyId)









