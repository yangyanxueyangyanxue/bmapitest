import ddt
import unittest
import time
import random
import string
from numpy import *
from common.urlToBase64 import Urltobase64
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
        #print(familyIds)
        pic_list_data = u.fm_pic_list(familyId)
        pic_list_code=pic_list_data.code
        pic_list=[]
        img_urllist=[]

        id=1 #网络图片
        if pic_list_code == 200:
            total = pic_list_data.data.total
            if total != 0:
                pic_data_list = pic_list_data.data.list
                for i ,item in  enumerate(pic_data_list):

                    pic_list.append(item['pic_id'])
                    img_urllist.append(item['img_url'])
                #print(pic_list)
            url=random.choice(img_urllist)


            photograph_save=u.photograph_save(familyIds,title,templateId,pic_list)
            photograph_save_code=photograph_save.code
            if photograph_save_code==200:
                photograph_save_id=photograph_save.data.id
                print(photograph_save_id)

                #上传封面 图片转base64
                photoGraphId=10946
                extend='jpg'


                imgdata=Urltobase64(url)


                uploadbase64=u.service_tools_uploadbase64(photoGraphId,extend,imgdata)


                memory_album_list = u.memory_album_list(familyId)
                memory_album_list_code=memory_album_list.code
                if memory_album_list_code==200:
                    album_list_data=memory_album_list.data
                    if album_list_data != None:

                        for i ,item in enumerate(album_list_data[0]):
                            if photograph_save_id==int(item[id]):
                                print("创建影集成功，并且影集列表增加数据成功")









if __name__ == '__main__':
    unittest.main()


