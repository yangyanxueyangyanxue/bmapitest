# coding=utf-8
from common.configure import CONFIG
from urllib.parse import urljoin
import requests
from common.configure import CONFIG
from interface.inner import  Interface
from common.req import Req
#社区2.1版本app接口

class Community(Interface):
    def __init__(self,uid,token):
        super(Community, self).__init__()
        self.server = CONFIG["show"]
        self.uid = uid
        self.token = token
        data = {
            'token': token,
            'uid': uid,
        }
        self.set_data(data)
    def home_topic(self,type):
        # 话题列表接口
        url = "/api/v1/content/home-topic"
        p = {
            "token":self.token,
            "uid":self.uid
        }
        d={"type":type}
        return self.post(url,data=d,params=p)

