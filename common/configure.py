# coding=utf-8

"""
全局配置
需要使用配置的导入本模块的CONFIG即可
"""

import os
import json

_filename = 'config.json'
_cur_dir = os.path.dirname(__file__)
_config_path = os.path.normpath(os.path.join(_cur_dir, '../', _filename))

print('load config: %s' % _config_path)

with open(_config_path) as f:
    _config = json.load(f)

_TESTING_DICT = _config['testing']
TEST_KEY = 'env_internal'
ONLINE_KEY = 'env_online'

ENV_SELECT_TEST = _TESTING_DICT[TEST_KEY]
ENV_SELECT_ONLINE = _TESTING_DICT[ONLINE_KEY]

LAST_ENV = ENV_SELECT_TEST

CONFIG = _TESTING_DICT[LAST_ENV]
BATCH_P = []


def change_env(env):
    global CONFIG
    global ENV_SELECT_ONLINE
    global LAST_ENV

    if env != 'online' and env != 'test':
        raise ValueError('env only support value: online or test')

    if env == 'online':
        LAST_ENV = ENV_SELECT_ONLINE
        CONFIG = _TESTING_DICT[LAST_ENV]
        print("launch Online Env")

    if env == 'test':
        LAST_ENV = ENV_SELECT_TEST
        CONFIG = _TESTING_DICT[LAST_ENV]
        print("launch Test Env")
