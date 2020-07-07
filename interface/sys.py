from urllib.parse import urljoin
import requests
from common.configure import CONFIG
from interface.inner import  Interface
from common.req import Req

class sys(Interface):
    def __init__(self,uid,token):
        """

        接口公共参数
        """
        super(sys,self).__init__()
        self.uid = uid
        self.token = token
        self.server="http://test.app.babamama.cn/"

        data = {

            'token': token,
            'tuid': uid,

        }
        self.set_data(data)

    def sys_header(self,familyId):
        """

        1 首页得大入口（相册，纪念册，老照片...）
        """
        interface = '/api/v2/sys/header'
        d={'familyId':familyId}
        r=self.post(interface,data=d)
        return r