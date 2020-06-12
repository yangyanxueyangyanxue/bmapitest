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

话题评论
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


