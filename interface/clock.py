# coding=utf-8
from common.configure import CONFIG
from urllib.parse import urljoin
import requests
from common.configure import CONFIG
from interface.inner import Interface
from common.req import Req


# 打卡相关接口(app_2.0)
# 添加打卡类型 → 创建打卡 → 立即打卡
class Clock(Interface):
    def __init__(self, uid, token):
        super(Clock, self).__init__()
        self.server = CONFIG["APP"]
        self.uid = uid
        self.token = token
        data = {
            'token': token,
            'uid': uid
        }
        self.set_data(data)

    def clock_add_type(self,typeName):
        # 添加打卡类型接口
        url = "/api/v1/clock-in/add-type"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {
            'typeName': typeName,

        }
        return self.post(url, data=d, params=p)



    def family_users(self,familyId):
        # 获取家庭成员列表
        url = "/api/v1/clock-in/family-users"
        p = {"token": self.token,
            "uid": self.uid,

        }
        d = {"token": self.token,
            "uid": self.uid,
            "familyId": familyId,



             }
        return self.post(url, data=d, params=p)


    def add_event(self,typeId,familyId,rewardContent,rewardType,successCount,executorUid):
        # 创建打卡接口
        url = "/api/v1/clock-in/add-event"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {
            "typeId": typeId,
            "familyId": familyId,
            "rewardContent": rewardContent,
            "rewardType": rewardType,
            "successCount": successCount,
            "executorUid": executorUid
        }
        return self.post(url,data=d,params=p)

    def list(self, familyId):
        # 打卡列表接口
        url = "/api/v1/clock-in/list"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"familyId": familyId}
        return self.post(url,data=d,params=p)





    def clock_in(self, eventId):
        # 立即打卡接口
        url = "/api/v1/clock-in/clock-in"
        p = {
            "token": self.token,
            "uid": self.uid

        }
        d = {"eventId": eventId

             }
        return self.post(url,data=d,params=p)
