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
创建完家书后，发布成功后--浏览页面分享--出现放进相册
"""
class Family_memory(Interface):

    def __init__(self,uid,token):

        super(Family_memory, self).__init__()
        self.server = CONFIG["album"]
        self.uid = uid
        self.token = token
        data = {
            'token': token,
            'uid': uid,
        }
        self.set_data(data)

    def fm_pic_list(self,familyId,page=1):
        """

        获取家庭下所有照片接口
        家书列表页面打开创建接口，首先请求这个，家书下增加照片请求这个接口
        """
        url="/api/v3/family-memory/pic-list"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"familyId": familyId,
             "page":page
             }
        return self.post(url, data=d, params=p)

    def fm_cate_list(self, familyId, page=1):
        #放进相册列表接口
        url = "/api/v3/family-memory/cate-list"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"familyId": familyId,
             "page": page
             }
        return self.post(url, data=d, params=p)

    def fm_mobile_pic_cate(self, familyId, picId,cateId):
        # 放进相册操作接口
        url = "/api/v3/family-memory/mobile-pic-cate"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"familyId": familyId,
             "picId": picId,
             "cateId": cateId,
             }
        return self.post(url, data=d, params=p)

    def fm_family_list(self, familyId, type, userId,page):
        """
        相册首页接口
        :param familyId: int,家庭id
        :param type:int	维度 1时间 2主题
        :param userId:int	查找用户id
        :param page:int	页数
        :return:
        """

        url = "/api/v3/family-memory/family-list"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"familyId": familyId,
             "type": type,
             "userId": userId,
             "page": page,
             }
        return self.post(url, data=d, params=p)