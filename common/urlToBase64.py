# coding=utf-8
import base64
import requests
from io import BytesIO


# 图片转base64格式

def Urltobase64(url):

    #本地上传
    # image_path = 'C:\\Users\\Admin\\Desktop\\1.jpg'
    # image_path=img_url
    # with open(image_path,'rb') as f:
    #
    #     image = f.read()


    # 图片保存在内存
    response = requests.get(url)
    # 得到图片的base64编码
    ls_f=base64.b64encode(BytesIO(response.content).read())
    # 将base64编码进行解码
    imgdata=base64.b64decode(ls_f)
    a=str(base64.b64encode(imgdata), encoding='utf-8')
    return a
     #如果需要切割文件
    # file1=image_base64.split(';base64,')[1]
if __name__ == "__main__":
    url1='http://pic1.zhimg.com/v2-2eff82c094ab0ef22e305a7376ca6058_1200x500.jpg'
    a=Urltobase64(url1)
    print(a)