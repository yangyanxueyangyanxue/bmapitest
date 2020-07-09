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
# 删除家书的草稿箱

@ddt.ddt
class homebokk_deldraft(unittest.TestCase):
    # @unittest.skip
    @read_csv_dict("homebooklist.csv")
    def test_homebookdeldraft(self,uid,familyId,):

        """
        删除草稿箱接口
        """
        u = InterfaceCenter.get_user(uid)
        # homebook_home = u.homebook_home(familyId)
        #
        # homebook_home_code = homebook_home.code
        # homebook_home_data=homebook_home.data
        # homebook_home_message=homebook_home.message
        #
        # if homebook_home_code == 200:
        #     # 草稿箱id为0不会变，所以把list提出来
        #     idlist1 = []
        #     for i, item in enumerate(homebook_home_data):
        #         if item['id'] != '0':
        #             idlist1.append(item['id'])
        #     print('idlist1',idlist1)
        #     # return
        #     first = int(random.choice(idlist1))
        #     for i, item in enumerate(homebook_home_data):
        #         if item['id'] != first:
        #             total1 = item['total']  # 记录当前列表得家书得总数
        #

        homebook_homecate = u.homebook_homecate(familyId,cateId=0,page=1)
        homebook_homecate_code = homebook_homecate.code
        if homebook_homecate_code == 200:
            homecate_total=homebook_homecate.data.total
            if homecate_total != "0":
                id=homebook_homecate.data.list[0].id
                homebook_deldraft=u.homebook_deldraft(id)
                homebook_deldraft_code=homebook_deldraft.code
                if homebook_deldraft_code==200:
                    homebook_homecate1 = u.homebook_homecate(familyId, cateId=0, page=1)
                    homebook_homecate_code1 = homebook_homecate.code
                    if homebook_homecate_code1 == 200:
                        homecate_total2 = homebook_homecate1.data.total
                        print(homecate_total2)
                        homecate_total3=int(homecate_total2)+1
                        self.assertEqual(int(homecate_total), homecate_total3 )
                        print("1111",homecate_total3)

