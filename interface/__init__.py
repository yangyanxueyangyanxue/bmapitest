"""
动态导入interface目录下的所有接口相关模块
将会触发inner下元类的注册逻辑
"""

import os
import re
import importlib

local_path = os.path.dirname(__file__)

for root_path, _, file_list in os.walk(local_path):
    # 跳过__pycache__文件
    if root_path.endswith("__"):
        continue
    # 路径替换，将interface之前的字符串删除，并将'/'替换成'.'
    module_path = '.'.join(re.sub(r'^.+?(interface)', r'\1', root_path).split('/'))
    for file_name in file_list:
        if not file_name.endswith('.py'):
            continue
        module_name = file_name[:-3]
        if module_name == "__init__" or module_name == "inner" or module_name == "sns":
            continue
        importlib.import_module("." + module_name, module_path)