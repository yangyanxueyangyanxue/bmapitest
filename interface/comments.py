# coding=utf-8
from common.configure import CONFIG
from urllib.parse import urljoin
import requests
from common.configure import CONFIG
from interface.inner import  Interface
from common.req import Req
#社区2.1版本app接口
"""
逻辑是，
1，新建的动态可以删除，删除后，查看首页是否还在，查看个人页面是否还在
2.新建一个动态--审核--展示在社区首页和个人主页--新建一个话题pk话题--动态放入话题里，点赞，分享，评论，pk选择
3.新建一个普通话题，动态放入话题，点赞，分享，评论
4.新建一个投票话题，动态放入话题，点赞，分享，评论，投票选择，再次投票
5.放入话题后，查看话题详情，修改话题
"""
class Comments(Interface):

    def __init__(self,uid,token):

        super(Comments, self).__init__()
        self.server = CONFIG["show"]
        self.uid = uid
        self.token = token
        data = {
            'token': token,
            'uid': uid,
        }
        self.set_data(data)

    def Comments_add_comment(self,cate_id,com_detail):

        #主题下得评论接口

        url="/api/v1/content/share-cate"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"cate_id": cate_id,
             "com_detail":com_detail}
        return self.post(url, data=d, params=p)


