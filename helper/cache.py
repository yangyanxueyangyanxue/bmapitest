# coding=utf-8

"""
缓存数据
减少请求
"""

from common.log import logger

_data = {}


def set(k, v):
    # logger.debug('update cache: %s' % k)
    _data[k] = v


def get(k):
    # logger.debug('hit cache: %s' % k)
    return _data.get(k)


def has(k):
    return k in _data
