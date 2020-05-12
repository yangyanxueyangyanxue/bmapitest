# coding=utf-8

"""
提供获取用户的方法
"""
from common.checker import success
from common.configure import CONFIG
from common.log import logger
from common.util import hl, hl_bg, FONT_RED
from helper import cache
from interface.sns import SNS
from interface.bind import Bind
from interface.inner import Interface
from model.usermodel import InterfaceModel
import interface

import json
import os
import random
import hmac
import requests
import uuid
import hashlib
import traceback
import io
import numpy as np

from universe import ROOT_DIR

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)

class UserFactory(object):
    """
    用户账户管理
    """
    user_file_path = os.path.join(ROOT_DIR, CONFIG['users_json_file_name'])

    @staticmethod
    def set_user_file(user_file_name):
        UserFactory.user_file_path = ROOT_DIR + "/users/" + user_file_name
        logger.debug(UserFactory.user_file_path)
        if not os.path.exists(UserFactory.user_file_path):
            raise FileNotFoundError("file " + user_file_name + " is not found in users")


    @classmethod
    def get_user_by_uid(cls, uid, token, package = "BBMM"):
        """
        通过uid获取用户
        """
        assert cls.is_token_valid(uid, token), 'token invalid'
        return InterfaceModel({
            'uid': uid,
            'token': token,
            "package": package
        })

    @classmethod
    def get_user(cls, uid):
        """
        获取用户
        """
        uidStr = str(uid)

        if cache.has(uid):
            return cache.get(uid)

        # uid
        user_model = cls.get_user_by_account(uid)
        cache.set(uidStr, user_model)
        return user_model

    @classmethod
    def get_user_by_account(cls, uid):
        """
        通过账号获取用户
        本地获取不到则通过密码登录
        """
        logger.info('user account: %s uid:%s' % (uid))
        try:
            u = cls.get_user_from_local(uid)
        except AssertionError as err:
            if uid is '':
                logger.error("get user failed: %s" % err)
                raise Exception(err)
            u = cls.get_user_from_login(uid)
        except Exception as err:
            logger.error("get user failed: %s" % err)
            raise Exception(err)
        return u

    @classmethod
    def _get_local_data(cls, name):
        """
        获取本地用户数据
        """
        with open(cls.user_file_path) as f:
            data = json.load(f)

        return data.get(name)

    @classmethod
    def get_user_from_local(cls, uid):
        """
        从本地数据获取用户
        """
        info = cls.get_local_user_info(uid)
        return InterfaceModel(info)

    @classmethod
    def get_user_from_login(cls, uid):
        """
        直接通过密码登录获取用户
        将数据存储在本地
        """
        assert uid, 'password empty'
        cls.update_token(uid)
        info = cls._get_local_data(uid)
        return InterfaceModel(info)

    @classmethod
    def get_local_user_info(cls, uid):
        """
        获取本地用户信息
        并验证token
        """
        user = cls._get_local_data(uid)
        assert user, 'user %s not exist' % uid

        uid = user.get('uid')
        token = user.get('token')
        package = user.get("package", "BBMM")

        if not cls.is_token_valid(uid, token):
            logger.info('token invalid')
            assert 'password' in user, 'password empty'
            cls.update_token(uid, package)
            user = cls._get_local_data(uid)
        return user

    @classmethod
    def get_user_info(cls, name):
        pass

    @classmethod
    def get_user_full_info(cls, uid, token):
        """
        从服务器获取用户全部信息
        """
        it = interface.user.User(uid, token)
        r = it.get_user_info(uid)
        return r['data']['user']['user_info']

    @classmethod
    def update_token(cls, uid,  package = "BBMM"):
        """
        更新本地token
        """
        r = cls.get_new_token(uid,  package)
        data = {
            'token': r[0],
            'uid': r[1],
            'package': package
        }
        cls._update_data(uid, data)
        return r

    @classmethod
    def get_new_token(cls, uid, package):
        """
        链接数据库获取最新token
        (token, uid)
        """
        # cm = CMAccount(package)
        # r = cm.login(uid)
        # sso_token = r['data']['sso_token']
        #
        # Interface.package = package
        # sns = interface.sns.SNS(sso_token)
        # r = sns.login_cm()
        # assert success(r), r

        token = r['data']['token']
        uid = r['data']['user']['user_info']['uid']

        return (token, uid)

    @classmethod
    def _update_data(cls, uid, info):
        """
        更新本地存储的token
        """
        with open(cls.user_file_path) as f:
            data = json.load(f)

        # 增加新用户
        if uid not in data:
            data[uid] = info
            need_update = True
        # 更新老用户
        else:
            old_info = data[uid]
            need_update = False

            for k, v in info.items():
                if (k in CONFIG['local_user_info'] or k in old_info) \
                        and old_info.get(k) != v:
                    # 处理中文问题
                    v = v.encode('utf-8')
                    old_info[k] = v
                    hl('update %s' % k)
                    need_update = True

        if need_update:
            with io.open(cls.user_file_path, 'w', encoding='utf8') as f:
                # ensure_ascii，encoding, 处理中文
                logger.debug("fk" + str(data))
                s = json.dumps(data, cls=MyEncoder, indent=4, sort_keys=True,
                               ensure_ascii=False)  # remove python3.x不支持的encoding='utf8'
                f.write(s)

    @classmethod
    def is_token_valid(cls, uid, token):
        """
        验证token是否有效，不区分主包、中东包、美国包
        #用create_video接口进行测试
        用/bind/get来验证
        """
        if not uid or not token:
            logger.debug('uid or token null')
            return False
        I = Bind(uid, token)
        r = I.get_bind()
        if r['msg'] == 'token error' or r['status'] != '200':
            logger.info('token error')
            return False
        return True



    @classmethod
    def check_local_data(cls):
        """
        更新所有本地数据
        脚本调用
        """
        with open(cls.user_file_path) as f:
            data = json.load(f)

        for name in data:
            try:
                hl_bg('\n * %s' % name)
                user = cls.get_local_user_info(name)
                uid, token = user['uid'], user['token']

                info = cls.get_user_full_info(uid, token)
                cls._update_data(name, info)
                logger.debug(info)
            except Exception:
                hl(('update %s failed' % name), FONT_RED)
                traceback.print_exc()


class CMAccount(object):
    """
    公司账号系统
    """

    def __init__(self, package = "LiveMe"):
        package_info = {
            "liveme": ["135301", "gL2FGHsJ"],
            "royallive": ["759350", "n1ATEoUJ"],
            "alive": ["213669", "3hGpPPId"]
        }

        appid, appsalt = package_info[package.lower()]
        android_id = 'testandroid'

        _uuid = str(uuid.uuid4())
        rand = random.randint(10000, 99999)
        sidstrs = str(rand) + _uuid + android_id + appsalt

        self.sid = self._sidstr(sidstrs)

        temp = hmac.new(bytes(appsalt.encode('utf-8')), bytes(self.sid.encode('utf-8')), hashlib.sha1).digest()
        import base64
        temp_bytes = base64.b64encode(temp)
        final_str = temp_bytes.decode()
        self.sig = self._replace_str(
            final_str.rstrip()
        )
        self.headers = {"appid": appid, "sid": self.sid, "sig": self.sig}

    '''改成你自己的逻辑  --小雪'''
    def login(self, uid):
        # url = "http://proxy.ksmobile.com/1/cgi/login"
        # url = "http://iag.ksmobile.net/1/cgi/login"
        url = "http://qa_iag.ksmobile.net/1/cgi/login"
        d = {'uid': uid}
        r = requests.post(url, data=d, headers=self.headers).json()
        # assert r['ret'] is 1, r
        return r

    def register(self, name, pwd):
        # url = "https://proxy.ksmobile.com/1/cgi/register"
        # url = "https://iag.ksmobile.net/1/cgi/register"
        url = "http://qa_iag.ksmobile.net/1/cgi/register"
        d = {'name': name, 'password': pwd}
        r = requests.post(url, data=d, headers=self.headers).json()
        return r

    def refresh(self, sid):
        """
        获取sso_token
        这个sid不是uid
        应该是需要获取到用户唯一的sid才可以
        暂时无用
        """
        url = "http://proxy.ksmobile.com/1/cgi/refresh"
        # url = "http://proxy.ksmobile.com/1/cgi/refresh"
        # url = "http://iag.ksmobile.net/1/cgi/refresh"
        url = "http://qa_iag.ksmobile.net/1/cgi/refresh"
        d = {'sid': sid}
        r = requests.post(url, data=d, headers=self.headers).json()
        return r

    def _sidstr(self, s):
        sid_str = hashlib.md5()
        sid_str.update(s.encode("utf-8"))
        return sid_str.hexdigest()

    def _replace_str(self, s):
        sig = ""
        for i in s:
            if i == "+":
                i = "-"
            elif i == "/":
                i = "_"
            elif i == "=":
                i = ""
            sig += i
        return sig
    # def ..

class CMAccountAPI(object):
    #问下客户端开发？？？
    def __init__(self, package=""):
        self.client_info = {
            "bbmm": {
                "Version-Name": "1.8.1",
                "Version-Code": "181",
                "Device-Type": "2"
            },

            }

        self.package = package

