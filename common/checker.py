# coding=utf-8
"""
数据相关操作
结果数据检查处理
"""

import json
from common.configure import CONFIG
from collections import OrderedDict

# 存储每次运行的接口对比数据
CHECK_DATA = {}
BAD_STATUS = {}


def is_json(self, s):
    try:
        json.loads(s)
    except ValueError as e:
        return False
    return True


def get_json(filepath):
    """
    取得整个json数据
    """
    with open(filepath) as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    return data


def get_json_data(filepath, key):
    """
    取json中的一个数据项
    """
    data = get_json(filepath)
    return data[key]


def format_json_file(filepath):
    with open(filepath) as f:
        s = json.load(f)

    with open(filepath, 'w') as f:
        json.dump(s, f, indent=4)


def _status_ok(s):
    """
    判断结果状态码是否为success
    """
    return str(s).lower() == '200'


def success(json_data):
    """
    json结果是否表示成功
    """
    return _status_ok(json_data['status'])


def _compare_data(data1, data2, key='', diff_data=None, ignore=None):
    """
    对比数据的结构、类型
    data1 new, data2 old
    返回差异结果
    TODO: 逻辑太乱，有待简化
    """

    if not ignore:
        ignore = set()

    if key in ignore or _should_ignore(key):
        logger.info('ignore field: %s' % key)
        return diff_data

    if diff_data is None:
        diff_data = [set(), set(), set()]  # 类型不一致，多的，少的

    if not same_type(data1, data2):
        info = '%s - %s' % (type(data1), type(data2))
        # print(info)
        diff_data[0].add((key, info))  # 字段，类型差异信息
        return diff_data

    # 已到最底层
    if isinstance(data1, str) or isinstance(data1, int):
        return diff_data

    # 如果是list，只比较第一个
    if isinstance(data1, list):
        if data1 and data2:
            _compare_data(data1[0], data2[0], key, diff_data, ignore=ignore)
        return diff_data

    # 剩下的是dict
    s1 = set(data1.keys())
    s2 = set(data2.keys())

    # 少的字段
    less = s2 - s1
    # info = 'lack fields: %s' % (','.join(less))
    # print(info)
    for k in less:
        k = '.'.join((key, k))
        if k in ignore or _should_ignore(k):
            print('ignore %s' % k)
            continue
        diff_data[2].add(k)

    # 多的字段
    more = s1 - s2
    # info = 'more fields: %s' % (','.join(more))
    # print(info)
    for k in more:
        k = '.'.join((key, k))
        if k in ignore or _should_ignore(k):
            print('ignore %s' % k)
            continue
        diff_data[1].add(k)

    # 共有字段
    common = s1.intersection(s2)
    for k in common:
        new_id = k if not key else '%s.%s' % (key, k)
        _compare_data(data1[k], data2[k], new_id, diff_data, ignore=ignore)

    return diff_data


def _should_ignore(s):
    """
    判断一个字段是否应该忽略
    """
    ignore_keys = CONFIG.get('ignore_fields', set())
    for k in ignore_keys:
        if k in s:
            return True
    return False


def compare(api, data1, data2):
    """
    对接口数据结构进行比对
    data1: new
    data2: old
    """
    print('\n* %s' % api)

    ignore = {
        "live.nearby": [],
        "live.homepagenew": [],
        "live.newmaininfo": []
    }

    ig = ignore.get(api)
    if ig:
        ig = set(ig)
        print('igonre: %s' % ig)

    diff = _compare_data(data1, data2, ignore=ig)
    return diff


def same_type(obj1, obj2):
    return type(obj1) == type(obj2)


if __name__ == '__main__':
    f1 = '../data/user.getinfo'
    f2 = '../data/user.getinfo2'
    data1 = get_json(f1)
    data2 = get_json(f2)

    compare('user.getinfo', data1, data2)
