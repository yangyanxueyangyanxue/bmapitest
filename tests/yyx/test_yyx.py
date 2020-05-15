import ddt
import unittest

from common import read_csv_dict
from model.factory import InterfaceCenter
user_file='yyx.json'
InterfaceCenter.set_user_file(user_file)

@ddt.ddt
class Yyx(unittest.TestCase):
    #@unittest.skip
    @read_csv_dict("body_form")
    def test_user_first(self,**data):
        pass

if __name__=='__main__':
    unittest.main()