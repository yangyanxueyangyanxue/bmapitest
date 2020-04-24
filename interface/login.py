# coding=utf-8
from interface.inner import Interface


class Guest(Interface):
    def __init__(self):
        super(Guest, self).__init__()

    def device_login(self, client_id, pwd, sign, timestamp, tongdun_black_box, trace_id, device_id, device_type,
                     ver3, ver4, data_type='301',):
        # 1:绑定，3: 忘记密码，4: 注册或验证码方式登录，5: 只发送短信
        uri = "/sns/deviceLogin"
        data = {
            "client_id": client_id,
            "pwd": pwd,
            "sign": sign,
            "timestamp": timestamp,
            "tongdun_black_box": tongdun_black_box,
            "transaction_id": trace_id,
            "data[from]": data_type

        }
        headers = {
            "xd": device_id
        }
        params = {
            "os": device_type,
            "ver": ver3,
            "vercode": ver4
        }
        return self.post(uri, data=data, headers=headers, params=params)