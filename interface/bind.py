# coding=utf-8


from interface.inner import Interface


class Bind(Interface):
    """
    验证token是否有效
    """
    def __init__(self, uid, token):
        super(Bind, self).__init__()
        self.uid = uid
        self.token = token
        data = {
            'token': token,
            'tuid': uid
        }
        self.set_data(data)
    '''
    记得改接口调用新项目的token地址  --小雪
    '''
    def get_bind(self):
        interface = '/bind/get'
        d = {
            'tuid': self.uid,
        }
        r = self.post(interface, data=d)
        return r
