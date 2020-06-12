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
话题点赞
"""
class Praise(Interface):

    def __init__(self,uid,token):

        super(Praise, self).__init__()
        self.server = CONFIG["show"]
        self.uid = uid
        self.token = token
        data = {
            'token': token,
            'uid': uid,
        }
        self.set_data(data)

    def Praise_praise(self,comment_id):

        #主题下得评论接口

        url="/api/v1/praise/praise"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"comment_id": comment_id,
             }
        return self.post(url, data=d, params=p)


