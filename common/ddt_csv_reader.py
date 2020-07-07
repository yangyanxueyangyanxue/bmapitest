import ddt
import csv
import inspect

__READ_TYPE_TUPLE = 1000
__READ_TYPE_DICT = 2000

__all__ = ('read_csv_tuple', 'read_csv_dict', "get_list_dict_from_csv", "get_list_tuple_from_csv")


def __get_data_from_csv(file_path, read_type):
    if read_type != __READ_TYPE_TUPLE and read_type != __READ_TYPE_DICT:
        raise Exception("read_type ----- > __READ_TYPE_TUPLE or __READ_TYPE_DICT")
    val_rows = []
    f_csv = None
    try:
        with open(file_path, encoding='UTF-8') as f:
            if read_type == __READ_TYPE_TUPLE:
                f_csv = csv.reader(f)
                next(f_csv)
            if read_type == __READ_TYPE_DICT:
                f_csv = csv.DictReader(f)
            for row in f_csv:
                val_rows.append(row)
    except FileNotFoundError:
        print("your csv file not found,my sister!please clock your file path")
    return val_rows


def get_list_dict_from_csv(file_full_path, module_path=None):
    global __READ_TYPE_DICT
    frm = inspect.stack()[1]
    module = inspect.getmodule(frm[0])
    pre_module_file_path = module.__file__
    if module_path is None:
        final_module_path = pre_module_file_path
    else:
        final_module_path = module_path
    file_full_path = __get_file_full_path(final_module_path, file_full_path)
    return __get_data_from_csv(file_full_path, __READ_TYPE_DICT)


def get_list_tuple_from_csv(file_full_path, module_path=None):
    global __READ_TYPE_TUPLE
    frm = inspect.stack()[1]
    module = inspect.getmodule(frm[0])
    pre_module_file_path = module.__file__
    if module_path is None:
        final_module_path = pre_module_file_path
    else:
        final_module_path = module_path
    file_full_path = __get_file_full_path(final_module_path, file_full_path)
    return __get_data_from_csv(file_full_path, __READ_TYPE_TUPLE)


def __my_ddt(*functions):
    def deco(f):
        for fun in reversed(functions):
            f = fun(f)
        return f

    return deco


def read_csv_tuple(csv_file_path, module_path=None):
    frm = inspect.stack()[1]
    module = inspect.getmodule(frm[0])
    pre_module_file_path = module.__file__
    if module_path is None:
        final_module_path = pre_module_file_path
    else:
        final_module_path = module_path
    return __real_wrapper(read_csv_tuple, csv_file_path, final_module_path)

def read_csv_dict(csv_file_path, module_path=None):
    frm = inspect.stack()[1]
    module = inspect.getmodule(frm[0])
    pre_module_file_path = module.__file__
    if module_path is None:
        final_module_path = pre_module_file_path
    else:
        final_module_path = module_path
    return __real_wrapper(read_csv_dict, csv_file_path, final_module_path)


def __real_wrapper(fun, csv_file_name, module_path):
    if module_path is not None:
        csv_file_name = __get_file_full_path(module_path, csv_file_name)
    wrapper = __get_wrapper(fun, csv_file_name)
    return wrapper


def __get_wrapper(func, csv_file_path):
    global __READ_TYPE_TUPLE
    global __READ_TYPE_DICT
    real_type = 0
    if func is read_csv_tuple:
        real_type = __READ_TYPE_TUPLE
    elif func is read_csv_dict:
        real_type = __READ_TYPE_DICT

    wrapper = __my_ddt(ddt.data(*__get_data_from_csv(csv_file_path, real_type)), ddt.unpack)

    return wrapper


def __get_file_full_path(current_module_path, file_name):
    import os
    return os.path.join(os.path.dirname(current_module_path), file_name)
