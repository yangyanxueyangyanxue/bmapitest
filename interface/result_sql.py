# coding=utf-8
from common.configure import CONFIG
from urllib.parse import urljoin
import requests
from common.configure import CONFIG
from interface.inner import  Interface
from common.req import Req
#社区2.1版本app接口

class Result_sql(Interface):
    def __init__(self):
        super(Result_sql, self).__init__()
        self.server = CONFIG["Result"]

    def batch(self):

        """

        批次号获取
        """
        url = "automation/batch"


        return self.get(url)

    def insertData(self,batchId,caseId,requestUrl,method,params,resp,cost,result,message):
        """
        插入接口测试结果 接口
        batchId	int	是	运行批次
        caseId	String	是	用例名称
        requestUrl	String	是	请求路径
        method	String	是	请求方式
        params	String	是	请求参数
        resp	String	是	响应数据
        cost	double	是	接口响应时间
        result	int	是	接口测试结果 0 ：pass 1：fail
        message	String	是	接口失败相关信息
        """
        url = "automation/insertData"
        data = {
            "batchId": batchId,
            "caseId": caseId,
            "requestUrl": requestUrl,
            "method": method,
            "params": params,
            "resp":resp,
            "cost": cost,
            "result": result,
            "message": message,


        }

        return self.get(url, data=data)


