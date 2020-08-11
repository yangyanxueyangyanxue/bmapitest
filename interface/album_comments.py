# coding=utf-8
from common.configure import CONFIG
from urllib.parse import urljoin
import requests
from common.configure import CONFIG
from interface.inner import  Interface
from common.req import Req
#相册2.6.2版本优化评论回复接口
"""
逻辑是，

话题评论
"""
class Album_Comments(Interface):

    def __init__(self,uid,token):

        super(Album_Comments, self).__init__()
        self.server = CONFIG["album"]
        self.uid = uid
        self.token = token
        data = {
            'token': token,
            'uid': uid,
        }
        self.set_data(data)

    def Album_Comments_add_comment(self,content_id,home_id,com_detail,soundId,isBigViewMode=None,):
        """
        评论接口
        comment_id 是 int 评论id

        content_id 是 int 内容id

        home_id 是 int 家庭id

        isBigViewMode 否 int 1/0 是否是大图模式评论

        com_detail 是 string 内容

        soundId  是 int 音频id


        """

        url="/api/v3/comments/add-comment"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"content_id": content_id,
             "home_id": home_id,
             "com_detail":com_detail,
             "soundId": soundId,
             "isBigViewMode": isBigViewMode,
             }
        return self.post(url, data=d, params=p)

    def Album_Comments_add_reply(self,comment_id,content_id,home_id,target_uid,rep_detail,soundId,):
        """
        回复接口
        comment_id 是 int 评论id

        content_id 是 int 内容id

        home_id 是 int 家庭id

        target_uid 是 int 回复目标uid

        rep_detail 是 string 内容

        soundId  是 int 音频id

        contentVoice 否 string 音频url

        duration 否 string 音频时长

        """
        url="/api/v3/comments/add-reply"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"comment_id": comment_id,
            "content_id": content_id,
             "home_id": home_id,
             "target_uid": target_uid,
             "rep_detail":rep_detail,
             "soundId": soundId,

             }
        return self.post(url, data=d, params=p)
