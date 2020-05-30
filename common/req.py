#coding=utf-8
"""
基础请求体
"""
from common.log import logger

import requests
import time

class Req(object):
    def __init__(self,empty=False):
        self.header={}
        self.params={}
        self.data={}
        #用request.session 实现keep alive
        #但是这样只是单一得接口keep alive
        #考虑通过urllib3 实现公用得connection pool
        self._req=requests.Session()
    def set_header(self,h=None):
        if h is None:
            h={}
        self.header.update(h)

    def set_params(self,p=None):
        if p is None:
            p={}
        self.params.update(p)

    def set_data(self,data=None):
        if data is None:
            data={}
        self.data.update(data)

    def post(self,path,**kwargs):
        return self.requests('Post',path,**kwargs)

    def get(self,path,**kwargs):
        return self.requests('Get',path,**kwargs)

    def requests(self,*args,**kwargs):
        """

        封装requests请求
        返回response请求

        """
        logger.debug('args:%s' % str(args))
        logger.debug('kwargs: %s' % str(kwargs))


        start_time=time.time()
        res=self._req.request(*args,**kwargs,verify=False)
        end_time=(time.time()-start_time)*1000
        self._req.close()
        #logger.info('time:%d % end_time')
        logger.debug('response:%s'% res.text)
        return res




