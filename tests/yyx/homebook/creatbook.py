import ddt
import unittest

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
    @read_csv_dict("creathomebook.csv")
    def test_creat_homebook(self,uid,familyId):

        """
        1.点击首页纪念册图标--查看home接口，首页得信息
        2.创建家书-保存到草稿箱，(首页)
        3。添加照片，删除草稿，删除章节
        4.发布
        5.发布成功后查看详情
        6.查看是否在首页feed流
        7.编辑家书，重新发布
        """
        u = InterfaceCenter.get_user(uid)
        homebook_home = u.homebook_home(familyId)

        homebook_home_code = homebook_home.code
        homebook_home_data=homebook_home.data
        homebook_home_message=homebook_home.message

        if homebook_home_code == 200:
            print('请求接口成功' ,homebook_home_data)
            homebook_home_total1=homebook_home_data[0]['total'] #记录当前草稿箱得数量
            #选择照片pic_list，选择得是家庭相册照片，没有用upload接口，这个接口是把手机照片传到服务器，转给对应得接口
            pic_list=u.fm_pic_list(familyId)
            pic_list_code=pic_list.code
            if pic_list_code==200:
                total=pic_list.data.total
                if total!=0:

                    img_url1=pic_list.data.list[0]['img_url']
                    img_url2=pic_list.data.list[1]['img_url']
                    print(img_url1, img_url2)


            #选择纪念册类型，然后返回二级或者三级标签得值 cate_auth
            #保存到草稿箱
            #编辑过程中，请求text_check接口校验
        else :
            print(homebook_home_code ,homebook_home_message)







if __name__ == '__main__':
    unittest.main()
