# coding=utf-8

from threading import Thread
from functools import partial
import os
import rsa
import base64

# 字体色
FONT_BLK = 30   # 黑
FONT_RED = 31   # 红
FONT_GRN = 32   # 绿
FONT_YLW = 33   # 黄
FONT_BLU = 34   # 蓝
FONT_PPL = 35   # 紫
FONT_DPG = 36   # 深绿
FONT_WHT = 37   # 白


def hl(s, color=FONT_YLW):
    # windows不支持颜色
    if os.name == 'nt':
        return s
    print('\033[%dm%s\033[0m' % (color, s))


def hred(s, color=FONT_RED):
    # windows不支持颜色
    if os.name == 'nt':
        return s
    print('\033[%dm%s\033[0m' % (color, s))


def hblu(s, color=FONT_BLU):
    # windows不支持颜色
    if os.name == 'nt':
        return s
    print('\033[%dm%s\033[0m' % (color, s))


def hppl(s, color=FONT_PPL):
    # windows不支持颜色
    if os.name == 'nt':
        return s
    print('\033[%dm%s\033[0m' % (color, s))


def hl_bg(s, color=0):
    # windows不支持颜色
    if os.name == 'nt':
        return s
    print('\033[44m%s\033[0m' % (s,))


def py_version():
    import sys
    info = sys.version_info
    ver = info[0] + info[1]/10.0
    return ver


def exec_threading(n, func, *args, **kvargs):
    """
    多线程并发
    适用于同一个普通函数或者对象方法
    """
    if isinstance(func, list):
        # 直接传入了func list
        # 是多个方法的并发
        # 忽略n
        jobs = func
    else:
        # 否则是同方法并发
        # 根据n生成func list
        f = partial(func, *args, **kvargs)
        jobs = [f for i in range(n)]

    rs = []
    def do(f):
        r = f()
        rs.append(r)

    ts = []
    for job in jobs:
        t = Thread(target=do, args=(job,))
        t.daemon = True
        ts.append(t)
        t.start()

    for t in ts:
        t.join()
    return rs


def bind_func(func, *args, **kvargs):
    """
    生成绑定方法
    可用于并发调用
    """
    return partial(func, *args, **kvargs)


def ansync(func):
    """
    异步（线程）装饰器
    """
    from threading import Thread
    from functools import wraps

    @wraps(func)
    def async_func(*args, **kwargs):
        t = Thread(target=func, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
        return t
    return async_func

def encrypt_pwd(password, public_key):
    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_key)
    crypto = rsa.encrypt(password.encode(), public_key)
    return base64.b64encode(crypto)