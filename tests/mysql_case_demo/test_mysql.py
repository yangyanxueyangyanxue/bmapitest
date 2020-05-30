import unittest
import ddt
# 数据库相关具体操作统一放到 dao 内，并暴露接口，dao 模块下还有具体的使用说明，请移步 /common/dao 模块
from common import dao
from common import db_conf

@ddt.ddt
class MysqlCase(unittest.TestCase):
    uid = "10715"
    #phone_number = "18701528054"
    # 数据库增、删、改、查四种相关操作的使用方法
    # @unittest.skip
    def test_mysql_select(self):
        result = dao.select_username_by_uid_and_phone(self.uid)

        for res in result:
            print(res.token,res.uid, res.nickname,)

    @unittest.skip
    def test_mysql_update(self):
        set_dict = {
            "username": "wang"
        }
        dao.update_username_by_uid_and_phone(self.uid, self.phone, set_dict)

    @unittest.skip
    def test_mysql_delete(self):
        dao.delete_by_uid_and_phone(self.uid, self.phone)

    @unittest.skip
    def test_mysql_insert(self):
        insert_data = {
            "uid": "123",
            "username": "xxxxxx",
            "phone_number": "987654321"
        }
        dao.insert_into_users(insert_data)

if __name__ == "__main__":
    unittest.main()