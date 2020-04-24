import ddt
import unittest
from model.factory import InterfaceCenter
user_file='yyx.json'
InterfaceCenter.set_user_file(user_file)

@ddt.ddt
class Yyx(unittest.TestCase):
    #@unittest.skip
    @read_csv_dict("body_form")
    def test_user_first(self,**data):
      """

      :param data:
      :return:
      """
        login_name=""
        interface=InterfaceCenter.get_interface(login_name)
        print(interface.get_user_info())

if __name__=='__main__':
    unittest.main()