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
class Content(Interface):

    def __init__(self,uid,token):

        super(Content, self).__init__()
        self.server = CONFIG["show"]
        self.uid = uid
        self.token = token
        data = {
            'token': token,
            'uid': uid,
        }
        self.set_data(data)

    def share_cate(self,cate_id):

        #主题分享落地页  cate_id		主题id

        url="/api/v1/content/share-cate"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"cate_id": cate_id}
        return self.post(url, data=d, params=p)

    def home_topic(self,type):

        # 话题列表接口 type 0首页 1发布页

        url = "/api/v1/content/home-topic"
        p = {
            "token":self.token,
            "uid":self.uid
        }
        d={"type":type}
        return self.post(url,data=d,params=p)

    def content_vote(self,topicId,itemId):

        # 话题列表接口
        # topicId		话题id
        # itemId		投票选项id

        url = "/api/v1/content/home-topic"
        p = {
            "token":self.token,
            "uid":self.uid
            }
        d= {"topicId":topicId,
           "itemId":itemId
            }
        return self.post(url,data=d,params=p)

    def comments_complaint(self,commentId):

        # 评论举报接口 commentId		评论/回复id

        url = "/api/v1/content/home-topic"
        p = {
            "token":self.token,
            "uid":self.uid
        }
        d={"commentId":commentId}
        return self.post(url,data=d,params=p)

    def comments_theme(self,type,cateId,page=1):

        # 话题详情接口

        url = "/api/v1/content/theme"
        p = {
            "token":self.token,
            "uid":self.uid
        }
        d={"type":type,
           "cateId":cateId,
           "page":page}
        return self.post(url,data=d,params=p)

    def comments_content(self,content_id):
        url = "/api/v1/content/content"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"content_id": content_id,}

        return self.post(url, data=d, params=p)

    def Comments_home(self,page):

        #主题下得评论接口

        url="/api/v2/content/home"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"page": page,
             }
        return self.post(url, data=d, params=p)

    def Comments_save(self, cateIds,title,content,syncAlbum='false'):
        # 主题下发布动态


        url = "/api/v1/content/save"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"cateIds[]": cateIds,
             "title": title,
             "content": content,
             "syncAlbum": syncAlbum,

             }
        return self.post(url, data=d, params=p)
