# coding=utf-8
from common.configure import CONFIG
from urllib.parse import urljoin
import requests
from common.configure import CONFIG
from interface.inner import  Interface
from common.req import Req
#首页feed流
class Feed(Interface):

    def __init__(self,uid,token):

        super(Feed, self).__init__()
        self.server = CONFIG["APP"]
        self.uid = uid
        self.token = token
        data = {
            'token': token,
            'uid': uid,
        }
        self.set_data(data)

    def Feed_list(self,familyId,start=0,page=1,limit=10,):
        """

        首页信息流接口，发布照片，发布家书，等动态
        """
        url = "/api/v2/feed/lists"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"familyId": familyId,
             "start":start,
             "page":page,
             "limit":limit

             }
        return self.post(url, data=d, params=p)