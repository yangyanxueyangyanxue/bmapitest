"""
接口demo
"""

from interface.inner import Interface

class CMS(Interface):
    def __init__(self):
        super(CMS, self).__init__()
        self.params.clear()
        self.headers.clear()

    def user_updateCountrycode(self, uid, countrycode):
        """
        管理后台更新用户终身国家码
        """
        interface = '/Services/user/updateCountrycode'
        d = {
            'uid': uid,
            'countrycode': countrycode
        }
        r = self.post(interface, data=d)
        self.params.update({
            "countyCode": countrycode
        })
        return r

    def adminlive_shelvesVideo(self, vid, type_value='online'):
        '''
        视频上架
        '''
        interface = '/Services/AdminLive/shelvesVideo'
        p = {
            'videoid': vid,
            'type': type_value,
        }
        r = self.post(interface, params=p)
        return r