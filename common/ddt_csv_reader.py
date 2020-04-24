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
        print("your csv file not found,my sister!please check your file path")
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
