## 安装
python 3.7

## 结构  
```
.
├── common      # 基础组件
├── helper      # 测试辅助，缓存、mock等
├── interface   # 服务端接口
├── model       # 用户数据模型
├── service     # 后端服务的测试客户端
├── users       # 测试账号
└── tests       # unittest用例
```

## 一个最终的测试用例如下  
```python
# 使用用户模型
test_user.py

def test_get_user_info(self):
    '''
    查询用户信息
    '''
    login = 'hiwz@fluxer.tv'                # 使用一个本地配置的账号
    u = InterfaceCenter.get_user(login)     # 获得该账号的用户
    r = u.get_user_info(u.uid)              # 该用户执行查询用户信息操作
    info = r.data.user.user_info            # 得到的结果数据

    assert info.uid == u.uid                # 对结果字段进行验证
    assert info.is_verified == '3'
    assert info.nickname.lower() == u.name.lower()

# 使用接口模型
test_interface.py

def test_get_actions_infos(self):
    '''
    查询背包活动信息
    '''
    i = InterfaceCenter.get_interface()     # 获得所有非登录接口的实例
    r = i.get_actions_infos()               # 获取背包活动信息
    data = r.data                           # 得到的结果数据

    assert r.status == "200"                # 对返回码进行校验
    assert data["901"].action_id == 901     # 对结果字段进行验证
```
## 用户模型
InterfaceCenter.get_user返回即为用户模型，可以调用所有登录接口。

## 接口模型
InterfaceCenter.get_interface返回即为接口模型，可以调用所有非登录接口

### 用户模型主要处理如下事情：
1. 账号数据维护，即token的检测和更新
2. 登录接口动作的封装。不同的接口可能由不同的测试人员维护，但是每个人可能都会使用到其他接口，用户模型将各个接口中的方法封装到一个模型中。
3. 获取该用户对应的（后端服务）测试客户端

### 接口模型主要处理如下事情：
所有非登录接口的封装。不同的接口可能由不同的测试人员维护，但是每个人可能都会使用到其他接口，接口模型将各个接口中的方法封装到一个模型中。

即，用户模型以及接口模型是一个统一的出口，封装了所有接口在业务层面上的种种动作和数据。


## 接口
interface.inner.Interface为所有接口的基类。

定义了网络请求的模板，并提供了一些可以定制流程的hook。

## 配置
### config.json
测试相关配置，如域名、通用请求参数，日志级别等

测试前请确认这些内容

### users/test_users.json
测试需要使用到的账号，InterfaceCenter.get_user需要使用这里的账号数据。数据要求为json格式。 

## 用例设计
应该尽量满足以下目标：
- 用例内不做硬编码，所需的数据（如账号、对比数据）放到外部独立文件
- 掌握参数化方法，通过外部文件配置的数据来驱动测试
- 用例分类，如应该有可直接运行线上环境的基础功能验证用例

## 代码规范
你的代码也许要被其他人使用，务必遵从规范！
- 完备的注释
  - 接口类的每个方法，写清楚用途。如果需要多行注释，则第一行为简要概括。
  - 测试用例类的docstring中写明该类的测试范围
  - 测试方法写明该用例的测试点
  - 提交git写明提交内容
- 命名
  - 测试用例文件命名为test_xxx.py，全小写，下划线分割
  - 测试方法命名test_xxname，全小写，下划线分割
  - 变量命名全为小写，下划线分割格式
