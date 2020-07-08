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
    @read_csv_dict("creathomebook.csv")
    def test_creat_homebook(self,uid,familyId,content,cateId,sort,type,videoUrl,picType):

        """
        家书创建的一种路径：
        首页--家书首页--笔按钮--创建--发布--并且查看列表数据增加
        """
        u = InterfaceCenter.get_user(uid)
        homebook_home = u.homebook_home(familyId)

        homebook_home_code = homebook_home.code
        homebook_home_data=homebook_home.data
        homebook_home_message=homebook_home.message

        if homebook_home_code == 200:
            #草稿箱id为0不会变，所以把list提出来
            idlist1=[]
            for i,item in enumerate(homebook_home_data):
                if item['id'] !='0':
                    idlist1.append(item['id'])
            # print('idlist1',idlist1)
            # return
            first = int(random.choice(idlist1))
            for i,item in enumerate(homebook_home_data):
                if item['id'] !=first:
                    total1=item['total'] #记录当前列表得家书得总数


            id=first
            homebook_cateauth=u.homebook_cateauth(familyId,id)
            homebook_cateauth_code=homebook_cateauth.code
            if homebook_cateauth_code == 200:
                idlist2 = []
                homebook_home_data_list=homebook_cateauth.data.list
                for i, item in enumerate(homebook_home_data_list):

                    idlist2.append(item['id'])
                print(idlist2,'idlist2')
                second = random.choice(idlist2)  # 随机取一个二级标签
                occurTime=a=int(time.time())

                print('请求接口成功' ,homebook_home_data)
                homebook_home_total1=homebook_home_data[0]['total'] #记录当前草稿箱得数量
                #选择照片pic_list，选择得是家庭相册照片，没有用upload接口，这个接口是把手机照片传到服务器，转给对应得接口
            else:
                print("homebook_cateauth_code",homebook_cateauth_code)
            pic_list=u.fm_pic_list(familyId)
            pic_list_code=pic_list.code



            if pic_list_code==200:
                total=pic_list.data.total
                if total!=0:

                    img_url1=pic_list.data.list[0]['img_url']
                    img_url2=pic_list.data.list[1]['img_url']
                    print(img_url1, img_url2)

                    pic_id_list=[]
                    pic_list_list=pic_list.data.list
                    for i, item in enumerate(pic_list_list):
                        pic_id_list.append(item['pic_id'])
                    pic_id= random.choice(pic_id_list)
                    print(pic_id ,'pic_id')
                    # save 接口家书id，
                    imageUrl=img_url1
                    picId=pic_id
                    cateName=""
                    unique=pic_id

                    savedraft = u.homebook_savedraft(familyId,picId,content,sort,type,cateName,
                           cateId,picType,unique,first) #保存草稿成功
                    savedraft_code=savedraft.code
                    savedraft_message = savedraft.message
                    if savedraft_code==200:
                        draftId=savedraft.data.id
                        print(draftId,1111)
                        cateId="0" #查看草稿箱列表是否多1
                        home_cate=u.homebook_homecate(familyId,cateId,page=1)
                        home_cate_code=home_cate.code
                        if home_cate_code==200:
                            home_cate_data_list=home_cate.data.list
                            print(home_cate_data_list)
                            for i,item in enumerate(home_cate_data_list):

                                if int(item['id'])== draftId:
                                    print("111")
                                #文本检测
                            text=content
                            text_check=u.homebook_textcheck(text)
                            text_check_code=text_check.code
                            if text_check_code==200:

                                #发布家书：
                                coverId=pic_id
                                title=content
                                imgUrl=img_url1
                                save=u.homebook_save(familyId,coverId,title,first,
                                draftId,sort,picId,imgUrl,type,id=None,
                                second=None,occurTime="",occurLocation="",content="",
                                cateId="",cateName="",videoUrl="")
                                save_code=save.code
                                if save_code==200:
                                    save_data_id=save.data.id #家书id
                                    homebook_home1 = u.homebook_home(familyId)

                                    homebook_home_code1 = homebook_home1.code
                                    homebook_home_data1 = homebook_home1.data


                                    if homebook_home_code1 == 200:
                                        for i, item in enumerate(homebook_home_data1):
                                            if first == item['id']:
                                                total2 = int(item['total'])
                                                self.assertEqual(( total2-1), int(total1))
                                            print("创建家书ok")
                                    else:
                                        print('homebook_home_code1',homebook_home_code1)
                                else:
                                    print("save_code",save_code)

                            else:
                                print("text_check_code",text_check_code)
                        else:
                            print("home_cate_code",home_cate_code)





                    else:
                        print(savedraft_code,)

            else:
                print("pic_list_code",pic_list_code)

            #选择纪念册类型，然后返回二级或者三级标签得值 cate_auth
            #保存到草稿箱
            #编辑过程中，请求text_check接口校验
        else :
            print(homebook_home_code ,homebook_home_message)







if __name__ == '__main__':
    unittest.main()
