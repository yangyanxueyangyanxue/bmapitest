# coding=utf-8

import os
import json
import logging
import logging.config

ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '../'))
CFG_PATH = os.path.join(ROOT_DIR, 'config.json')


def setup_logging():
    try:
        with open(CFG_PATH) as f:
            data = json.load(f)
        log_config = data['log']
        logging.config.dictConfig(log_config)
    except Exception as e:
        logging.basicConfig(level=logging.INFO)
        logging.warning('log setup failed', exc_info=True)


class _Logger(object):
    """
    封装标准的logger
    功能未实现
    """
    def __init__(self):
        self._instance = None
        self._stack = []

        setup_logging()
        self._instance = logging.getLogger(__name__)
        self._instance.info('logger init')

    def __getattr__(self, name):
        return getattr(self._instance, name)

    def push_stack(self, s):
        """
        log stack
        用于异常定位时输出详尽信息
        """
        self._stack.append(s)

    def clear(self):
        self._stack = []

    def print_stack(self):
        for line in self._stack:
            self.warning(line)


# logger为单例
# 使用时from log import logger
logger = _Logger()
