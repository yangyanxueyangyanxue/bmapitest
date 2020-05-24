# coding=utf-8
"""
用户级别的操作行为
是接口请求的封装
"""

from common.log import logger
from common.util import hl
import os
from interface.inner import Interface, interface_class, login_required_class

def get_target_interface():
    final_dict = {}
    root_dir_path = os.path.dirname(__file__)
    will_work_dir = os.path.abspath(os.path.join(root_dir_path, "../interface"))
    for mainDir, subDir, file_name_list in os.walk(will_work_dir):
        def element_reform(val):
            point_str = '.py'
            if not val.endswith(point_str):
                del val
            else:
                tail_length = len(point_str)
                return val[:len(val) - tail_length]

        all_module_name = map(element_reform, file_name_list)
        import importlib
        from interface.inner import Interface
        for eleModule in all_module_name:
            if eleModule is None or eleModule == '__init__' or eleModule == 'allload' or eleModule == 'inner' or eleModule == 'temp' or eleModule == 'sns' or eleModule == 'mars' or eleModule == 'bags' or eleModule == 'services':
                continue
            module = importlib.import_module("." + eleModule, 'interface')
            attr_list = dir(module)
            final_class = None
            for attr in attr_list:
                obj = getattr(module, attr)
                if isinstance(obj, type) and issubclass(obj, Interface) and obj is not Interface:
                    final_class = obj
                    break
            final_dict[eleModule] = final_class
        break
    return final_dict


class InterfaceModel(object):

    """
    用户操作对象
    业务动作放到相关接口文件内
    """

    def __init__(self, user_info = {}):
        self.uid = user_info.get('uid')
        self.token = user_info.get('token')
        self.name = user_info.get('nickname')
        self.package = user_info.get("package", "BBMM")

        # 归属个人的通用请求数据
        # todo: 是否interface中的数据直接引用user的更合理？
        self._data = {}
        self._params = {}
        self._headers = {}

        self._init_interface()

    def _init_interface(self):
        """
        初始化各种接口对象
        """
        self.TARGET_INTERFACE_INSTANCE_DICT = {}  # 接口对象
        self.TARGET_METHOD_DICT = {}  # 接口方法
        for keyModuleName, valClassName in interface_class.items():
            self._add(keyModuleName, valClassName)

    def _add(self, module_name, interface_class_name):
        """
        加入接口集合
        """
        Interface.package = self.package
        if module_name in login_required_class:
            interfaceInstance = interface_class_name(self.uid, self.token)
        else:
            interfaceInstance = interface_class_name()
        self.TARGET_INTERFACE_INSTANCE_DICT[module_name] = interfaceInstance
        # 增加接口方法
        self._add_method(interfaceInstance)

    def _add_method(self, interface_obj):
        """
        初始化所有可以调用的接口实例方法
        """

        attr_method_doc_nest_list = self._get_all_user_method(interface_obj)
        for eachEle in attr_method_doc_nest_list:
            attr_name, method_instance, doc = eachEle
            assert attr_name not in self.TARGET_METHOD_DICT, 'duplicate interface method: %s'% attr_name
            self.TARGET_METHOD_DICT[attr_name] = (method_instance, doc)

    def __getattr__(self, name):
        """
        遍历所有接口，提供相应方法调用
        """
        assert name in self.TARGET_METHOD_DICT, 'method not found: %s' % name
        method_index = 0
        method_obj = self.TARGET_METHOD_DICT[name][method_index]
        # logger.debug('%s.%s called' % (m.im_class, name))
        #  print('%s.%s called' % (m.im_class, name))
        return method_obj

    def _get_all_user_method(self, interface_obj):
        """
        从各个接口类中提取用户可以操作的方法
        """
        base_inner_attr_list = dir(Interface)
        user_funcs = []

        for attr_name in dir(interface_obj):
            if not callable(getattr(interface_obj, attr_name)):
                continue
            # 排除基类中的
            if attr_name in base_inner_attr_list:
                continue
            if attr_name.startswith('_'):
                continue
            user_funcs.append(attr_name)
        filter_method_nest_list = []
        for attr_name in user_funcs:
            method_obj = getattr(interface_obj, attr_name)
            doc = method_obj.__doc__
            doc = doc.strip().split('\n')[0] if doc else 'None'
            filter_method_nest_list.append((attr_name, method_obj, doc))
        return filter_method_nest_list

    def set_req(self, data=None, params=None, headers=None):
        """
        设置人的通用请求数据，用于直接调用request
        """
        if data:
            self._data.update(data)
        if params:
            self._params.update(params)
        if headers:
            self._headers.update(headers)

    def get_all_user_actions(self):
        """
        所有用户可以进行的操作
        """
        hl('<User Model>')
        ims = self._get_all_user_method(self)
        for im in ims:
            name, m, doc = im
            # print('%s:\n\t%s' % (name, doc))

        for it in self.TARGET_INTERFACE_INSTANCE_DICT.values():
            hl(it.__class__)
            ims = self._get_all_user_method(it)
            for im in ims:
                name, m, doc = im
                # print('%s:\n\t%s' % (name, doc))

    def post(self):
        """
        不经过接口层封装直接发请求
        """
        pass

    def get(self):
        pass

    def request(self, path, params=None, data=None, headers=None):
        """
        直接使用接口基类
        方便一些数据驱动的测试
        """
        from interface.inner import Interface

        req = Interface()
        # 跟随人的通用数据
        req.set_data(self._data)
        req.set_params(self._params)
        req.set_headers(self._headers)

        r = req.post(path, params=params, data=data, headers=headers)
        return r

    def get_client(self, name):
        """
        获取user对应的后端服务client
        """
        if name == 'relation':
            from service.relation import Relation
            return Relation(self.uid)
        elif name == 'im':
            from service.im.client import TcpClient
            return TcpClient(self.uid, self.token)
        assert 0, 'no service: %s' % service


if __name__ == '__main__':
    pass
