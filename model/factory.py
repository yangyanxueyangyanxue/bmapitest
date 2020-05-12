from model.usermodel import InterfaceModel
from model.user_factory import UserFactory

class InterfaceInstanceFactory:
    """
    接口实例化工厂
    """
    def __getattr__(self,name):
        """

        用户类型单独走用户工厂
        """
        return getattr(UserFactory,name)

    def get_interface(self,username=None,password =''):

        """

        其他类型直接创建接口类实例
        """
        #接口实例需要登陆的情况下，还是通过用户工厂创建实例

        if username is not None:
            return UserFactory.get_user(username)

#创建工厂实例
InterfaceCenter=InterfaceInstanceFactory()
InterfaceCenter=InterfaceCenter