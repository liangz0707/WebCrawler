# coding: utf-8
import requests
import json
from bs4 import BeautifulSoup
import os

import pickle
requests.adapters.DEFAULT_RETRIES = 5  
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

#生成时间戳保证下载的内容文件名不重复
import time
def getT():
    t = time.time()
    s = str(int(t*100%10000000))
    return s


main_url = ""
mainc = ""
import urlparse
title_list= [] #保存所有要爬取帖子的链接
for i in range(1,2):
    p ="/?9.html"
    if i != 1 :
        p  = "/?9-%d.html" % (i)
    l = main_url+p
    print l

    req = requests.get(l) #得到一个页面
    page = req.text #得到页面文本
    soup = BeautifulSoup(page,'html.parser')
    a_list = soup.find_all("a")
    hrefs = [t.get("href") for t in a_list if t.get("target") and t.get("target")=='_blank' and 'article' in t.get("href")]
    title_list.extend(hrefs)
title_list = [urlparse.urljoin(mainc,t) for t in title_list ]
#title_list = title_list[0:5]#节省时间 ，暂时先用前几个帖子
print "\n".join(title_list)
print 'c'
image_url_list = [] #保存所有获取到图片的url 供之后下载
for t_url in title_list: #处理每一个主题页面
    print t_url
    req = requests.get(t_url)
    page = req.text
    soup = BeautifulSoup(page,'html.parser')
    im_list = soup.find_all("img") #先获取图片元素
    im_list = [t.get("src") for t in im_list if t.get("src")[-3:]=='jpg' and 'article' in  t.get("src") ]
    #print im_list
    image_url_list.extend(im_list)
print "\n".join(image_url_list)
#开始下载
for img_url in image_url_list :
    print img_url
    saveImage(img_url , getT()+".jpg")

