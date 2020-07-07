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
创建完家书后，发布成功后--浏览页面分享
"""
class Share(Interface):

    def __init__(self,uid,token):

        super(Share, self).__init__()
        self.server = CONFIG["album"]
        self.uid = uid
        self.token = token
        data = {
            'token': token,
            'uid': uid,
        }
        self.set_data(data)

    def share_commemorative(self,id,family):

        #家书分享

        url="/api/v3/share/commemorative"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"id": id,
             "family":family
             }
        return self.post(url, data=d, params=p)

    # def fm_cate_list(self, familyId, page=1):
    #     #放进相册列表接口
    #     url = "/api/v3/family-memory/cate-list"
    #     p = {
    #         "token": self.token,
    #         "uid": self.uid
    #     }
    #     d = {"familyId": familyId,
    #          "page": page
    #          }
    #     return self.post(url, data=d, params=p)

