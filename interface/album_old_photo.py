# coding=utf-8


from interface.inner import Interface


class Album_old_photo(Interface):
    """
    老照片激活页面接口
    """
    def __init__(self, uid, token):
        super(Album_old_photo, self).__init__()
        self.uid = uid
        self.token = token
        data = {
            'token': token,
            'uid': uid
        }
        self.set_data(data)

    def Album_old_photo_active(self,familyId,fromUid):
        interface = '/api/v3/family/old-photo-active'
        d = {"uid":self.uid,
             "token":self.token

        }
        p = {"familyId": familyId,
             "fromUid": fromUid

             }
        r = self.post(interface, data=d, params=p)

        return r
