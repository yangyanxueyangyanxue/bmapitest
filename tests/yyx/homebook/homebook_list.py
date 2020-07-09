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
# 从列表里取出数据，删除，点赞，评论，分享等操作

@ddt.ddt
class homebokk_list(unittest.TestCase):
    # @unittest.skip
    @read_csv_dict("homebooklist.csv")
    def test_homebooklist(self,uid,familyId,):

        """
        家书列表，评论增加，删除，点赞
        """
        u = InterfaceCenter.get_user(uid)
        homebook_home = u.homebook_home(familyId)

        homebook_home_code = homebook_home.code
        homebook_home_data=homebook_home.data
        homebook_home_message=homebook_home.message

        if homebook_home_code == 200:
            # 草稿箱id为0不会变，所以把list提出来
            idlist1 = []
            for i, item in enumerate(homebook_home_data):
                if item['id'] != '0':
                    idlist1.append(item['id'])
            print('idlist1',idlist1)
            # return
            first = int(random.choice(idlist1))
            for i, item in enumerate(homebook_home_data):
                if item['id'] != first:
                    total1 = item['total']  # 记录当前列表得家书得总数

            cateId = first
            homebook_homecate = u.homebook_homecate(familyId,cateId,page=1)
            homebook_homecate_code = homebook_homecate.code
            if homebook_homecate_code == 200:
                homecate_total=homebook_homecate.data.total
                if homecate_total != "0":
                    id=homebook_homecate.data.list[0].id
                    # 点赞
                    homebook_praise=u.homebook_praise(id,)
                    homebook_praise_code=homebook_praise.code
                    homebook_message=homebook_praise.message

                    if homebook_praise_code==200:
                        print("点赞成功",homebook_message)
                    else:
                        print("homebook_praise_code",homebook_praise_code)
                    #举报
                    homebook_report=u.homebook_report(id)
                    homebook_report_code = homebook_report.code
                    homebook_report_message = homebook_report.message
                    if homebook_report_code==200:
                        print("举报成功",homebook_report_message)
                    else:
                        print("homebook_report_code",homebook_report_code)
                    #添加评论
                    contentId=id
                    # 由于接口没有返回评论id，生成随机的字符串，去校验评论
                    alphabet = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*()'
                    comDetail = random.choice(alphabet)

                    homebook_addcomment=u.homebook_addcomment(contentId,comDetail)
                    homebook_addcomment_code=homebook_addcomment.code
                    if homebook_addcomment_code==200:

                        # 评论后列表增加数据
                        homebook_commentlist=u.homebook_commentlist(contentId,id=0)
                        homebook_commentlist_code=homebook_commentlist.code
                        if homebook_commentlist_code==200:
                            homebook_commentlist_list=homebook_commentlist.data.list
                            for i ,item in enumerate(homebook_commentlist_list):
                                if item['content']==comDetail:
                                    commentId=item['id']
                                    repUid=item['uid']
                            repDetail=comDetail
                            contentId=id
                            #回复评论
                            homebook_addreply=u.homebook_addreply(contentId,commentId,repUid,repDetail)
                            homebook_addreply_code=homebook_addreply.code
                            if homebook_addreply_code==200:
                                homebook_commentlist1 = u.homebook_commentlist(contentId, id=0)
                                homebook_commentlist_code1 = homebook_commentlist.code
                                if homebook_commentlist_code1 == 200:
                                    homebook_commentlist_list1 = homebook_commentlist.data.list
                                    for i, item in enumerate(homebook_commentlist_list1):
                                        if item['content'] == comDetail:


                                            print("111111yyx")
                            #删除评论或者回复
                            homebook_delcom=u.homebook_delcom(familyId, commentId,contentId)
                            homebook_delcom_code=homebook_delcom.code
                            if homebook_delcom_code==200:
                                homebook_commentlist2 = u.homebook_commentlist(contentId, id=0)
                                homebook_commentlist_code2 = homebook_commentlist.code
                                if homebook_commentlist_code2 == 200:
                                    homebook_commentlist_list2 = homebook_commentlist.data.list
                                    for i, item in enumerate(homebook_commentlist_list2):
                                        if item['content'] != comDetail:
                                            print("已经删除回复的内容")









                    else:
                        print("homebook_addcomment_code",homebook_addcomment_code)





                else:
                    print("该去请求pic_list接口，传照片，发布")



