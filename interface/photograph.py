# coding=utf-8
from common.configure import CONFIG
from urllib.parse import urljoin
import requests
from common.configure import CONFIG
from interface.inner import  Interface
from common.req import Req
import json
from numpy import *
#影集
class Photograph(Interface):

    def __init__(self,uid,token):

        super(Photograph, self).__init__()
        self.server = CONFIG["album"]
        self.uid = uid
        self.token = token
        data = {
            'netst': '1',
            'token': token,
            'tuid': uid,
            'app': 'BBMM'
        }
        self.set_data(data)
    def photograph_template(self):
        """

        影集模板列表接口 返回字段
        "id": "1",      //id
            "class": null,  //分类
            "class_name": "",  //分类名称
            "weights": "0",  //权重
            "title": "万物生长",  //影集名称
            "svga": "",
            "cover_size_small": "",  //封面-小
            "cover_size_big": "",  //封面-大
            "bgm_id": "0",  //bgm id
            "photo_tran": "",  //照片转场
            "canvas_tran": "",  //画布转场
            "status": "1",  //状态 0删除 1正常
            "created_at": "0",
            "updated_at": "0",
            "is_new":  0  //是否为新  0否 1是
        """
        url = "/api/v3/photograph/template"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {

             }
        return self.post(url, data=d, params=p)

    def photograph_effect(self):
        """
        影集效果图列表接口

        """
        url = "/api/v3/photograph/effect"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {

        }
        return self.post(url, data=d, params=p)

    def photograph_save(self,familyIds,title,templateId,pic_list):
        """
        发布影集
        familyIds	是	array	分享到的家庭id数组
        pics	是	array
        图片id及类型（0 本地图片 1网络图片）

        [

        [图片id => 类型],

        [图片id => 类型]

        ]

        eg：[[1,1][2,1],[3,0]]

        title	是	string	影集名称
        templateId	是	int	模板id

        """
        interface = "/api/v3/photograph/save"


        p = {
            "token": self.token,
            "uid": self.uid
        }

        keys = ['familyIds[]', 'title', 'templateId'];
        values = [familyIds, title, templateId];
        pics = array([(pic_list[0:3])])
        for x, item in enumerate(pics):
            a=len(pics[0])-1
            print(a,1)
            for i in range(a):
                #print(pics[x][i])
                keys.append('pics[' + str(x) + ']'+'['+str(i)+']');
                values.append(pics[x][i]); # 是下标得第一个第一个
                values.append(1);
            print('value',values)
            print('keys',keys)

        dictionary = dict(zip(keys, values))

        print(dictionary)
        r = self.post(interface, params=p, data=dictionary)
        return r

    def photograph_content(self,home_id,content_id):
        """
        影集详情接口
        home_id	是	int	家庭id
        content_id	是	int	动态id
        """
        url = "/api/v3/content/content"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"home_id":home_id,
             "content_id": content_id,


        }
        return self.post(url, data=d, params=p)
    def memory_album_list(self,familyId):
        """

        影集管理页列表接口


        """
        url = "/api/v3/memory/album-list"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"familyId": familyId,



             }
        return self.post(url, data=d, params=p)

    def service_tools_uploadbase64(self,photoGraphId,extend,file):
        """

        影集封面图上传
        Post 请求参数（支持json和form-data）
        photoGraphId
        是	int	影集id
        extend	是	strig	图片后缀 jpg，png等
        file	是	string	去掉前缀的 图片的base64编码

        """
        url = "/api/service/tools/uploadbase64"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"photoGraphId": photoGraphId,
            "extend": extend,
             "file": file,


             }
        return self.post(url, data=d, params=p)
