"""
管理后台接口
"""

from interface.inner import Interface
from common.configure import CONFIG
class Backstage(Interface):
    def __init__(self):
        super(Backstage, self).__init__()
        self.params.clear()
        self.headers.clear()
        self.server= CONFIG["album"]

    def bs_login(self,name,password):
        """
        管理后台登录
        """

        interface ='/admin/admin/user/login'
        d = {
            'name': name,
            'password': password
        }
        r = self.post(interface,data=d)
        # self.params.update({
        #     "countyCode": countrycode
        # })
        return r

