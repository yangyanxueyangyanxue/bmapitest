# coding=utf-8
from common.configure import CONFIG
from urllib.parse import urljoin
import requests
from common.configure import CONFIG
from interface.inner import  Interface
from common.req import Req
import json
#纪念册
class Home_book(Interface):

    def __init__(self,uid,token):

        super(Home_book, self).__init__()
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
    def homebook_home(self,familyId):
        """

        获取家书首页信息接口（打开家书首先请求这个接口）
        """
        url = "/api/v3/homebook/home"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"familyId": familyId,

             }
        return self.post(url, data=d, params=p)

    def homebook_tutorial(self, familyId):
        """

        家书教程图片接口
        """
        url = "/api/v3/homebook/tutorial"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {

             }
        return self.post(url, data=d, params=p)
    def homebook_homecate(self,familyId,cateId,page=1):
        """

        家书列表接口
        cateId:标签id
        """
        url="/api/v3/homebook/home-cate"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"familyId": familyId,
             "cateId":cateId,
             "page":page

             }
        return self.post(url, data=d, params=p)
    def homebook_save(self,familyId,coverId,title,first,draftId,sort,picId,imgUrl,type,
                      id=None,second=None,occurTime="",occurLocation="",content="",
                       cateId="",cateName="",videoUrl=""):
        """
        发布家书接口
        id	否	int	家书id（有家书id的话就是修改）
        familyId	是	int	家庭id
        coverId	是	int	封面id
        title	是	string	标题
        first  是	int	一级标签id
        second 否	int	二级标签id
        draftId	是	int	草稿箱id
        occurTime	否	int	发生时间
        occurLocation	否	string	发生地点
        list	是	string	小节
        """
        url = "/api/v3/homebook/save"
        list_params = [{


            "cateId": cateId,
            "content": content,
            "sort": sort,

            "cateName": cateName,
            "picId":picId,
            "imgUrl": imgUrl,
            "videoUrl": videoUrl,

            "type": type,

        }]
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"familyId": familyId,
             "id":id,
             "coverId": coverId,
             "title": title,
             "first":first,
             "draftId":draftId,
             "list":json.dumps(list_params),
             "second": second,
             "occurTime": occurTime,
             "occurLocation": occurLocation

             }
        return self.post(url, data=d, params=p)
    def homebook_textcheck(self,text):
        """

        文本检测接口，输入一个文本完就请求一次，保存也会请求
        """
        url = "/api/v3/homebook/text-check"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"text": text,

             }
        return self.post(url, data=d, params=p)

    def homebook_savedraft(self,familyId,picId,content,sort,type,cateName,
                           cateId,picType,unique,first,
                           id=None,contentId=None,cover="",coverType=None,title="",
                           imgUrl="",videoUrl="",
                           second="",occurTime="",occurLocation="",):
        """
        保存草稿箱接口，打开创建先请求一次，每隔30s自动请求一次
        id	否	int	草稿箱id
        contentId	否	int	家书id
        familyId	是	int	家庭id
        cover	否	string	封面id或者封面本地地址
        coverType	否	int	1oss 2本地
        title	否	string	标题
        list	是	string
        [{}]
        [
            "picId" => 1, // 图片视频id
         "content" => 1, // 小节描述
         "cateId" => 1, // 标签id
         "sort" => 1, // 排序
         "type" => 1, // 1图片 2视频
         "cateName" => "测试", // 标签名称
         "imgUrl" => "", // 图片url
         "videoUrl" => "", // 视频url
         "picType" => 1, // 1网络 2本地
         "unique" => "123", // 小节唯一码
        ]
        occurTime	否	int	发生时间
        occurLocation	否	string	发生地点
        first
        是	int	一级标签id
        second
        否	int	二级标签
        """
        list_params=[{
            "picId": picId,
            "content": content,
            "cateId": cateId,
            "sort": sort,
            "type": type,
            "cateName": cateName,
            "imgUrl": imgUrl,
            "videoUrl": videoUrl,
            "picType": picType,
            "unique": unique,
        }]
        #这里只是实现了，传一张网络图片信息,思路：写一遍  然后循环放到一个新的数组里 需要几组循环几次
        url = "/api/v3/homebook/save-draft"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"familyId": familyId,
             "id":id,
             "contentId":contentId,
             "cover":cover,
             "coverType":coverType,
             "title":title,
             "second":second,
             "occurTime":occurTime,
             "occurLocation":occurLocation,

             "list": json.dumps(list_params),
             "first": first,
             }
        return self.post(url, data=d, params=p)
    def homebook_query(self,id,familyId):
        """

        家书详情接口
        """
        url = "/api/v3/homebook/query"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"id": id,
             "familyId":familyId

             }
        return self.post(url, data=d, params=p)

    def homebook_cateauth(self,familyId,id):






        """
        获取标签下级列表及标签权限接口（草稿箱列表打开后请求这个接口）
        编辑草稿箱需求请求这个获取标签，一级，二级 首页选择编辑，选择好家书类型，接着请求二级标签
        id	是	int	标签id
        """
        url = "/api/v3/homebook/cate-auth"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"familyId": familyId,
             "id": id,
             }
        return self.post(url, data=d, params=p)
    def homebook_querydraft(self,id):
        """
         id:草稿箱id
        草稿箱打开得家书详情接口（草稿箱列表打开后请求这个接口）
        编辑家书详情接口
        """
        url = "/api/v3/homebook/query-draft"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"id": id,

             }
        return self.post(url, data=d, params=p)
    def homebook_deldraft(self,id):
        """
         id:草稿箱id
        删除草稿箱接口
        """
        url = "/api/v3/homebook/del-draft"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"id": id,

             }
        return self.post(url, data=d, params=p)
    def homebook_del(self,id):
        """
         id:家书id
        删除家书
        """
        url = "/api/v3/homebook/del"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"id": id,

             }
        return self.post(url, data=d, params=p)

    def homebook_addcomment(self, contentId,comDetail):
        """
         contentId:家书id
         comDetail:评论内容
        家书添加评论
        """
        url = "/api/v3/homebook/add-comment"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"contentId": contentId,
             "comDetail":comDetail

             }
        return self.post(url, data=d, params=p)
    def homebook_addreply(self, contentId,commentId,repUid,repDetail):
        """
            contentId	是	int	家书id
            commentId	是	int	被回复的评论id
            repUid	是	int	被回复的uid
            repDetail	是	string	回复内容
        家书添加回复
        """
        url = "/api/v3/homebook/add-reply"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"contentId": contentId,
             "commentId":commentId,
             "repUid":repUid,
             "repDetail":repDetail


             }
        return self.post(url, data=d, params=p)

    def homebook_commentlist(self, contentId, id):
        """
         家书的评论回复列表
         contentId	是	int	家书id
         id	是	int	第一次为0 是指第一页

        """
        url = "/api/v3/homebook/comment-list"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"contentId": contentId,
             "id": id

             }
        return self.post(url, data=d, params=p)

    def homebook_delcom(self, familyId, commentId,contentId):
        """
         家书删除评论或回复
         familyId	是	int	家庭id
        commentId	是	int	评论或回复id
        contentId	是	int	家书id

        """
        url = "/api/v3/homebook/del-com"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"familyId": familyId,
             "commentId": commentId,
             "contentId":contentId

             }
        return self.post(url, data=d, params=p)

    def homebook_praise(self, id):
        """
         点赞、取消点赞接口
         id	是	int	家书id

        """
        url = "/api/v3/homebook/praise"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"id": id,


             }
        return self.post(url, data=d, params=p)

    def homebook_share_commemorative(self, id,familyId):
        """
         获取家书(分享)详情接口
         id	是	int	家书id

        """
        url = "/api/v3/share/commemorative"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"id": id,
             "familyId":familyId

             }
        return self.post(url, data=d, params=p)

    def homebook_report(self, id):
        """
         家书举报接口
         id	是	int	家书id

        """
        url = "/api/v3/homebook/report"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"id": id,

             }
        return self.post(url, data=d, params=p)

    def homebook_queryalbumcate(self,id):
        """
         通过相册标签id获取家书标签id接口
         id	是	int	相册标签id

        """
        url = "/api/v3/homebook/query-album-cate"
        p = {
            "token": self.token,
            "uid": self.uid
        }
        d = {"id": id,


             }
        return self.post(url, data=d, params=p)