# coding=utf-8
#获取云曲库

from common.configure import CONFIG
from urllib.parse import urljoin
import requests
from common.configure import CONFIG
from interface.inner import  Interface
from common.req import Req
import json
from numpy import *


class Album_music(Interface):

    def __init__(self, uid, token):
        super(Album_music, self).__init__()
        self.uid = uid
        self.token = token
        data = {
            'token': token,
            'uid': uid
        }
        self.set_data(data)

    def Album_tencent_music_items(self,categoryId,page=1,size=10):
        """
        获取云曲库分类内容下歌曲列表接口
        """
        interface = '/v3/music/tencent-music-items'
        d = {"uid":self.uid,
             "token":self.token

        }
        p = {"categoryId": familyId,
             "page": page,
             "size": size,

             }
        r = self.post(interface, data=d, params=p)

        return r

    def Album_tencent_music_stations(self,page=1,size=10):
        """
        获取云曲库分类内容列表接口
        """
        interface = '/v3/music/tencent-music-stations'
        d = {"uid":self.uid,
             "token":self.token

        }
        p = {"page": page,
             "size": size

             }
        r = self.post(interface, data=d, params=p)

        return r

    def Album_tencent_music_id(self,id):
        """
        获取云曲库歌曲信息接口
        """
        interface = '/v3/music/tencent-music-id'
        d = {"uid":self.uid,
             "token":self.token

        }
        p = {"id": id,
            

             }
        r = self.post(interface, data=d, params=p)

        return r
