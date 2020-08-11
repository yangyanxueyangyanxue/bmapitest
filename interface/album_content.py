from common.csv_writer import writer_csv
from interface.inner import Interface
from common.configure import CONFIG
import json
import urllib
import numpy as np

#2.6.2版本的评论列表接口

class Album_content(Interface):
    def __init__(self):
        super(Album_content,self).__init__()
        self.params.clear()
        self.headers.clear()
        self.server = CONFIG["album"]
        self.uid = uid
        self.token = token

    def Album_content_comment(self,content_id,home_id):
        '''
        评论列表接口
        content_id	是	int	内容id
        home_id	是	int	家庭id
        '''
        interface = '/api/v3/content/content-comment'
        d = {

            'content_id': content_id,
            'home_id': home_id,

        }
        p = {
            'token': token,
            'uid':uid,

        }
        r = self.post(interface, params=p,data=d)
        return r