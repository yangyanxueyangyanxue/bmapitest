
from interface.inner import Interface
from common.configure import CONFIG
import json
import urllib
import numpy as np

#社区新建话题广告接口

class Backstage_ad(Interface):
    def __init__(self):
        super(Backstage_ad,self).__init__()
        self.params.clear()
        self.headers.clear()
        self.server=CONFIG["show"]

    def bs_cate_list(self,token,type,page=1,all=0):
        '''
        话题列表接口
        type:1普通 2投票 3PK
        '''
        interface = '/backend/v1/cate/cate-list'
        d = {

            'type': type,
            'page': page,
            'all':all
        }
        p = {
            'token': token,

        }
        r = self.post(interface, params=p,data=d)
        return r
    def bs_cate_cate_ad(self,token,page=1):
        '''
        广告管理中的话题列表接口

        '''
        interface = '/backend/v1/cate/cate-list'
        p = {
            'token': token,

        }
        r = self.post(interface, params=p)
        return r

    def bs_content_get_list(self, token,userId, cateId,nickname,startTime,endTime,page,export,userType):
        '''
        动态列表接口
        userId	否	int	用户id
        cateId	否	int	话题id
        nickname	否	string	生活秀昵称
        startTime	否	string	开始时间
        endTime	否	string	结束时间
        page	否	int	分页
        export	否	int	是否导出excel，默认0不导出，1导出
        userType	否	int	用户类型 不传表示不区分用户 1ugc用户(真实用户) 2pgc用户(即生活秀自己的内置用户)

        '''
        interface = '/backend/v1/cate/cate-list'
        p = {
            'token': token,

        }
        d={ 'userId': userId,
            'cateId': cateId,
            'nickname': nickname,
            'startTime': startTime,
            'endTime': endTime,
            'page': page,
            'export': export,
            'userType': userType,
            }
        r = self.post(interface, params=p,data=d)
        return r


    def bs_audit_cate_list(self, token,contentId,status,recomCate,recomHome,remark,homeStartTime,cateStartTime):
        '''
        动态列表接口
        contentId	是	int	作品id
        status	是	int	0禁用 1通过
        recomCate	否	int	0未推荐到主题 1推荐到主题
        recomHome	否	int	0未推荐到首页 1推荐到首页
        remark	否	string	作品备注
        homeStartTime	否	int	首页开始时间（时间戳）
        cateStartTime	否	int	话题开始时间

        '''
        interface = '/backend/v1/cate/cate-list'
        p = {
            'token': token,

        }
        d={ 'contentId': contentId,
            'status': status,
            'recomCate': recomCate,
            'recomHome': recomHome,

            'remark': remark,
            'homeStartTime': homeStartTime,
            'cateStartTime': cateStartTime,
            }
        r = self.post(interface, params=p,data=d)
        return r

    def bs_audit_operate(self, token,contentId, status,recomCate,recomHome,remark,
                         homeStartTime,cateStartTime,):
        '''
        动态审核接口
        contentId	是	int	作品id
        status	是	int	0禁用 1通过
        recomCate	否	int	0未推荐到主题 1推荐到主题
        recomHome	否	int	0未推荐到首页 1推荐到首页
        remark	否	string	作品备注
        homeStartTime	否	int	首页开始时间（时间戳）
        cateStartTime	否	int	话题开始时间

        '''
        interface = '/backend/v1/audit/operate'
        p = {
            'token': token,

        }
        d={ 'type': type,
            'contentId': contentId,
            'status': status,
            'recomCate': recomCate,
            'recomHome': recomHome,
            'remark': remark,
            'homeStartTime': homeStartTime,
            'cateStartTime': cateStartTime,

            }
        r = self.post(interface, params=p,data=d)
        return r

    def bs_update_status(self, token, id, status,):
        '''
        修改广告状态接口

        id	否	int	广告id（编辑时传）

        '''
        interface = '/backend/v1/ad/create'
        p = {
            'token': token,

        }
        d = {'id': id,
             'status': status,

             }
        r = self.post(interface, params=p, data=d)
        return r
    def bs_create(self, token,type, topic_id,position_topic_id,position_content_id,recommend,
                         up_date,sort,status,up_type,cover_url,jump_address,id,banner_type):
        '''
        新建广告接口
        type	是	int	广告类型 1Banner 2社区推荐 3话题推荐
        topic_id  否	int	展示话题ID
        position_topic_id否	int	位置话题ID
        position_content_id否	int	位置动态ID
        recommend否	int	推荐 0否 1是
        up_date否	int	最新 0否 1是
        sort否	int	位置序号
        status否	int	状态 0下架 1启用
        up_type否	int	类型 1话题 2动态
        cover_url否	string	封面图URL
        jump_address否	string/int	跳转地址
        id	否	int	广告id（编辑时传）
        banner_type	否	int	banner类型 1H5页面 2原生页面

        '''
        interface = '/backend/v1/ad/create'
        p = {
            'token': token,

        }
        d={ 'type': type,
            'topic_id': topic_id,
            'position_topic_id': position_topic_id,
            'position_content_id': position_content_id,

            'recommend': recommend,
            'up_date': up_date,
            'status': status,
            'up_type': up_type,
            'cover_url': cover_url,
            'jump_address': jump_address,
            'id': id,
            'banner_type': banner_type,
            }
        r = self.post(interface, params=p, data=d)
        return r

    def bs_create_cate(self,token,title,subtitle,content,thumbnail,background,sort,
                         status,type,items):
        '''
        新建话题接口
        title	是	string	标题
        subtitle	是	string	副标题
        content	是	string	简介
        thumbnail	是	string	缩略图 url
        background	是	string	背景图 url
        sort	是	int	排序
        status	是	int	状态 0删除 1正常
        type	是	int	1普通 2投票 3PK
        options	否	string	[{"item":"我"},{"item":"懒"},{"item":"啊"}]

        '''

        # d = {'title': title,
        #      'subtitle': subtitle,
        #      'content': content,
        #      'thumbnail': thumbnail,
        #      'background': background,
        #      'sort': sort,
        #      'status': status,
        #      'type': type
        #      }

        keys = ['title', 'subtitle', 'content', 'thumbnail', 'background', 'sort', 'status', 'type'];
        values = [title, subtitle, content, thumbnail, background, sort, status, type]
        if items is not None:
            itemList = items.split('_');
            for x, item in enumerate(itemList):
                keys.append('options['+str(x)+'][item]');
                values.append(item);
        dictionary = dict(zip(keys, values)) #将两个键值对得list转换成json，然后把json转换成字典格式
        interface = '/backend/v1/cate/create-cate'
        p = {
            'token': token,
        }

        r = self.post(interface, params=p, data=dictionary)
        return r



    def bs_set_cate_status(self, token, id, status,):
        '''
        话题状态修改接口

        id	是	int	话题id
        status	是	int	当前状态 0删除 1正常


        '''
        interface = '/backend/v1/cate/set-cate-status'
        p = {
            'token': token,

        }
        d = {'id': id,
             'status': status,

             }
        r = self.post(interface, params=p, data=d)
        return r
    def bs_query_cate(self, token, id, status,):
        '''
        话题详情接口

        id	是	int	话题id

        '''
        interface = '/backend/v1/cate/query-cate'
        p = {
            'token': token,

        }
        d = {'id': id,


             }
        r = self.post(interface, params=p, data=d)
        return r

    def bs_update_cate(self, token, id, title,subtitle,content,thumbnail,background,sort,status,
                       type,options):
        '''
        话题详情接口

        id	是	int	话题id
        title	否	string	标题
        subtitle	否	string	副标题
        content	否	string	简介
        thumbnail	否	string	缩略图
        background	否	string	背景图
        sort	否	int	排序
        status	否	int	状态 0删除 1正常
        type	是	int	1普通 2投票 3PK
        options	否	array	[{"item":"我","id":5},{"item":"懒","id":6}]


        '''
        interface = '/backend/v1/cate/update-cate'
        p = {
            'token': token,

        }
        d = {'id': id,
             'title': title,
             'subtitle': subtitle,
             'content': content,
             'thumbnail': thumbnail,
             'background': background,
             'sort': sort,
             'status': status,
             'type': type,
             'options': options,

             }
        r = self.post(interface, params=p, data=d)
        return r