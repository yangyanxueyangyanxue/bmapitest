# coding=utf-8
"""
接口基类
封装通用处理流程
"""
from common.configure import ENV_SELECT_TEST
from common.req import Req
from common.util import *
from common.checker import *
from common.log import *
import urllib.parse as url_parse
import time
import json

from urllib.parse import urljoin
from addict import Dict
import inspect

interface_class = {}
login_required_class = []
non_register_class = ["Interface", "SNS"]
alias_param = {
    "liveme": "lm",
    "royallive": "ar",
    "alive": "us"
}

class InterfaceMeta(type):
    """
    通过元类实现将所有子类注册到interface_calss
    需要登录的子类, 将会注册到login_required_class
    """
    def __new__(meta, name, bases, attrs):
        cls = type.__new__(meta, name, bases, attrs)
        if name in non_register_class:
            return cls
        assert name not in interface_class, 'add duplicate interface class %s'% name
        interface_class[name] = cls
        for attr_name, attr in attrs.items():
            if attr_name == "__init__" and "token" in inspect.getargspec(attr).args:
                login_required_class.append(name)
        return cls

class Interface(object, metaclass = InterfaceMeta):
    """
    接口模板
    所有请求都要经过这里
    """

    package = "com.bbmmgroup.www"

    def __init__(self):
        from common.configure import CONFIG
        self.req = Req()
        self.server = CONFIG['APP']
        self.data = {}
        self.params = {}
        self.headers = {}
        self.package = Interface.package

        # 提供些magic way
        self._remove = set()  # 请求时去除参数
        self._modify = {}  # 请求时更新参数

        # 通用参数
        headers = CONFIG.get('headers', {})
        headers['t'] = str(int(time.time() * 1000))
        params = CONFIG.get('params', {})

        self.set_headers(headers)
        self.set_params(params)

    def set_headers(self, headers):
        self.headers.update(headers)

    def set_params(self, params):
        self.params.update(params)

    def set_data(self, data):
        self.data.update(data)

    def modify_req_hook(self, rqd):
        """
        提交请求前对请求数据的加工处理
        可在各继承类中定义
        rqd是字典，可以访问和修改data, params, headers
        """
        pass

    def magic_way(self, rqd):
        """
        临时修改请求数据的magic方法
        一些测试用例会有此需求，如测试缺少默认参数
        """
        d, p, h = rqd['data'], rqd['params'], rqd['headers']
        # 更新参数
        if self._modify:
            for k in self._modify:
                for part in [d, p, h]:
                    if k in part:
                        part[k] = self._modify[k]
        # 排除的参数
        if self._remove:
            for k in self._remove:
                d.pop(k, None)
                p.pop(k, None)
                h.pop(k, None)

    def _request(self, method, path, **kwargs):

        # 可以指定服务器地址
        host = self.server
        url = urljoin(host, path)

        d, p, h = self._make_req_data(data = kwargs.get("data"), params = kwargs.get("params"), headers = kwargs.get("headers"))

        # modify hook
        rqd = {'data': d, 'params': p, 'headers': h}
        self.modify_req_hook(rqd)
        self.magic_way(rqd)
        d, p, h = rqd['data'], rqd['params'], rqd['headers']

        if d:
            kwargs["data"] = d
        kwargs["params"] = p
        kwargs["headers"] = h

        try:
            response = self.req.requests(method, url, **kwargs)
        except Exception as e:
            logger.warning(e)
            raise
        return self.handle_response(response)

    def handle_response(self, response):
        """
        响应处理
        默认返回json结果
        子类可重定义
        """
        try:
            r = response.json()
        except Exception as e:
            logger.warning('non json response\nstatus_code: {}\ncontent: {}\n'.format(response.status_code, response.content))
            # 如果不是json结果
            # 返回状态码和页面文本
            # 这块处理待改进
            return response.text

        # 接口数据结构对比
        if CONFIG.get("checker"):
            path = url_parse.urlparse(response.url).path
            # 拼接成a.b形式
            api = '.'.join(path.lower().strip('/').split('/'))
            check(api, r)
        return Dict(r)

    def _make_req_data(self, data = None, params = None, headers = None):
        """
        基础参数+自定参数
        """
        # shallow copy should be ok
        d = self.data.copy()
        p = self.params.copy()
        h = self.headers.copy()

        # 非登录接口不更新此参数
        # if p:
        #     p.update({
        #         "alias":alias_param[self.package.lower()]
        #     })

        # 基础参数+自定参数
        if data:
            d.update(data)
        if params:
            p.update(params)
        if headers:
            h.update(headers)
        return d, p, h

    def post(self, path, **kwargs):
        return self._request('POST', path, **kwargs)

    def get(self, path, **kwargs):
        return self._request('GET', path, **kwargs)


#
# 下面这些function应该挪走
#

def check(api, data):
    """
    接口校验
    """
    logger.debug(api)
    logger.debug(json.dumps(data))
    b = check_status(api, data)
    if b:
        check_local_data(api, data)


def check_status(api, data):
    """
    请求是否成功
    """
    if success(data):
        return True
    BAD_STATUS[api] = data
    return False


def check_local_data(api, data):
    """
    检查本地接口数据
    """
    fpath = get_data_path(api)
    # 记录全局数据
    R = CHECK_DATA

    # 新接口数据
    if not os.path.exists(fpath):
        # create new
        write_data(fpath, data)
        R[api] = None
        return

    # 比较新老数据
    old_data = get_json(fpath)
    diff = compare(api, data, old_data)

    # 出现差异，更新本地数据
    if is_diff(diff):
        R[api] = diff
        save_diff_data(fpath, data)

    if not api in R:
        R[api] = None


def is_diff(diff_data):
    """
    是否差异
    """
    return diff_data[0] or diff_data[1] or diff_data[2]


def save_diff_data(path, data):
    """
    保存有差异的接口数据
    备份原有数据，用新数据覆盖
    """
    import shutil
    bak_path = path + '.old'
    print('copy %s to %s' % (os.path.basename(path), os.path.basename(bak_path)))
    shutil.copy(path, bak_path)
    write_data(path, data)


def write_data(path, data):
    """
    写入接口数据文件
    """
    logger.info('write data: %s' % path)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def get_data_path(name):
    """
    接口数据文件path
    """
    data_dir = os.path.join(ROOT_DIR, 'data/%s' % ENV_SELECT_TEST)
    if not os.path.isdir(data_dir):
        try:
            os.makedirs(data_dir)
        except Exception as e:
            logger.error('create data dir failed')
            raise

    fpath = os.path.join(data_dir, name)
    return fpath

if __name__ == '__main__':
    print(ROOT_DIR)
