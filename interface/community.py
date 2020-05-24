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
        self.server = CONFIG["APP"]
        self.uid = uid
        self.token = token
        data = {
            'netst': '1',
            'token': token,
            'tuid': uid,
            'app': 'liveme'
        }
        self.set_data(data)
    def home_topic(self,type):
        # 1:绑定，3: 忘记密码，4: 注册或验证码方式登录，5: 只发送短信
        url = "/api/v1/content/home-topic"
        data = {
            "type": type,

        }
        # headers = {
        #     "xd": device_id
        # }
        # params = {
        #     "os": device_type,
        #     "ver": ver3,
        #     "vercode": ver4
        # }
        return self.post(url, data=data)
