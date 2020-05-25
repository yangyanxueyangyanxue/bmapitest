# coding=utf-8


from interface.inner import Interface


class Family(Interface):
    """
    验证token是否有效
    """
    def __init__(self, uid, token):
        super(Family, self).__init__()
        self.uid = uid
        self.token = token
        data = {
            'token': token,
            'tuid': uid
        }
        self.set_data(data)

    def get_family(self):
        interface = '/api/v1/family/lists'
        d = {
            'tuid': self.uid,
        }
        r = self.post(interface, data=d)
        return r
