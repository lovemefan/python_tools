# -*- codeing: utf-8 -*-
# @Time:2018/3/13 22:20
# @Author:lovemefan
# @File:一人之下漫画爬虫.py
# @Software:PyCharm
import os
from imp import reload
import re
import requests as requests
from urllib.request import urlretrieve

requestSession = requests.session()
# 保存一张图片
# 输入参数imgUrl 图片路径,imgPath 保存路径
def savePicture(imgUrl, imgPath):
    response = requests.get(imgUrl)
    codimg = response.content
    fn = open(imgPath, 'wb')
    fn.write(codimg)
    fn.close()

# 一人之下的漫画路径
url = "http://www.omanhua.com/comic/17521/"
html = requests.get(url)
html.encoding = 'UTF-8'
# print(html.text)
# 先获取每一话
# 先将数据块取出
bookListBlock = re.findall(r'<div class="subBookList">(.*?)</div></div>', html.text, re.S)
# booklist 为每一话的URL的列表
bookList = re.findall("</a></li><li><a href='(.*?)' title='(.*?)'", bookListBlock[0],re.S)

# 逐话操作
for index in bookList:
    indexUrl = "http://www.omanhua.com/"+index[0]+'index.html'
    indexHtml = requests.get(indexUrl)
    indexHtml.encoding = 'UTF-8'
    print(indexHtml.url)
    # 获得当前话的每张图片路径
    picList = re.findall("一人之下\|(.*?)'\.", indexHtml.text)[0].split('|')
    #删去piclist无用的信息
    for item in picList[:]:
        if item.__len__() != 10:
            picList.remove(item)

    print(index[1]+'共有%d页'%picList.__len__())
    picUrlRoot = u'http://pic.fxdm.cc/tu/undefined/一人之下/'
    # 指定存储位置
    location = "J:/一人之下"
    # 分开放图片
    # for page in range(len(picList)):
    #     if not os.path.exists("%s/%s/"%(location,index[1])):
    #         os.makedirs("%s/%s/"%(location,index[1]))
    #     picUrl = picUrlRoot+ index[1]+'/'+picList[page]+'.jpg'
    #     path = "%s/%s/%d.jpg"%(location,index[1],page)
    #     picUrl.encode('UTF-8')
    #     #不下载已经下载过的图片,便于更新
    #     if not os.path.exists(path):
    #         savePicture(picUrl,path)
    #         print(picUrl + ' 保存到了 ' + path)
    #

    # 一起放图片
    if not os.path.exists(location):
        os.makedirs(location)
    for page in range(len(picList)):
        picUrl = picUrlRoot+ index[1]+'/'+picList[page]+'.jpg'
        path = "%s/%s_%d.jpg"%(location,index[1],page)
        picUrl.encode('UTF-8')
        # 不下载已经下载过的图片,便于更新
        if not os.path.exists(path):
            savePicture(picUrl,path)
            print(picUrl + ' 保存到了 ' + path)


