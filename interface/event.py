from urllib.parse import urljoin
import requests
from common.configure import CONFIG
from interface.inner import  Interface
from common.req import Req

class excellentcover(Interface):
    def __init__(self,uid,token):
        """

        接口公共参数
        """
        super(excellentcover,self).__init__()
        self.uid = uid
        self.token = token
        self.server="http://test.app.babamama.cn/"

        data = {
            'netst': '1',
            'token': token,
            'tuid': uid,
            'app':'liveme'
        }
        self.set_data(data)

    def e_apply(self,act_id):
        """

        1 用户报名[返回用户信息]
        """
        interface = '/a1/excellentCover/apply'
        d={'act_id':act_id}
        r=self.post(interface,data=d)
        return r