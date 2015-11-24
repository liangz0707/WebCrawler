
# coding: utf-8

import requests

import json

from bs4 import BeautifulSoup


import os
def saveImage( imgUrl,imgName ="default.jpg" ):
    response = requests.get(imgUrl, stream=True)
    image = response.content
    DstDir=os.getcwd() #保存在当前工作目录下
    print("保存文件"+imgName+"\n")
    try:
        with open(os.path.join(os.getcwd(),'image',imgName) ,"wb") as jpg:
            jpg.write( image)
            return
    except IOError:
        print("IO Error\n")
        return
    finally:
        jpg.close


# In[55]:

#生成时间戳保证下载的内容文件名不重复
import time
def getT():
    t = time.time()
    s = str(int(t*100%10000000))
    return s


# #6.爬取百度贴吧图片

# In[71]:

#首先需要请求一个贴吧的主页
main_url = "http://tieba.baidu.com/f"
page_num = 3 #用与计算需要爬取的页数
title_list= [] #保存所有要爬取帖子的链接
for i in range(page_num): 
    params = {"kw" : "火影" , "pn":i*50} #通过页码和关键字决定
    req = requests.get(main_url,params=params) #得到一个页面
    page = req.text #得到页面文本
    soup = BeautifulSoup(page,'html.parser')
    a_list = soup.find_all("a")
    hrefs = [t.get("href") for t in a_list if t.get("class") and t.get("class")[0]=="j_th_tit"]
    title_list.extend(hrefs)
#print(title_list)


#进行url拼装
import urlparse
#url拼接的例子
#print urlparse.urljoin('http://somehost.com/', '../other/path')
#进行拼接
title_list = [urlparse.urljoin( main_url , t) for t in title_list]
#print title_list

#title_list = title_list[0:5]#节省时间 ，暂时先用前几个帖子
image_url_list = [] #保存所有获取到图片的url 供之后下载
for t_url in title_list: #处理每一个主题页面
    pn_num = 1 #先假设只有一页
    i=0
    while i< pn_num :
        i = i+1
        #设置页面参数
        param = {"see_lz" : 1 ,"pn":i+1}  #只抓取楼主的内容
        req = requests.get(t_url,param)
        page = req.text
        soup = BeautifulSoup(page,'html.parser')
        im_list = soup.find_all("img") #先获取图片元素
        im_list = [t.get("src") for t in im_list if t.get("class") and t.get("class")[0]=="BDE_Image"]
        image_url_list.extend(im_list)
        
        #获取真实的页数
        pnc = soup.find_all("span")
        pnc = [p.text for p in pnc if p.get("class")and p.get("class")[0] == "red"]
        pn_num =  int(pnc[1]) 
        
#print(image_url_list)

#开始下载
for img_url in image_url_list :
    saveImage(img_url , getT()+".jpg")


# In[ ]:



