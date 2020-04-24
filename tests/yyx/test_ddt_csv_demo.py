import unittest
import ddt
from common.ddt_csv_reader import *


@ddt.ddt
class MyCase(unittest.TestCase):
    from common.configure import LAST_ENV
    from common.configure import ENV_SELECT_ONLINE

    if LAST_ENV is ENV_SELECT_ONLINE:
        LOAD_FILE_NAME = "body_form_online.csv"
    else:
        LOAD_FILE_NAME = 'body_form.csv'

    @read_csv_dict(LOAD_FILE_NAME, __file__)
    def test_ddt_dict_demo(self, country, user, password):
        print("user--->:" + user)
        print("password---->:" + password)
        print("country----->:" + country)

    @read_csv_dict(LOAD_FILE_NAME)
    def test_ddt_dict_demo_second(self, **data):
        print(data)


if __name__ == "__main__":
    unittest.main()
