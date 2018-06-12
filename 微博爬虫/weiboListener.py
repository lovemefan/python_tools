# -*- codeing: utf-8 -*-
# @Time:2018/5/29 16:41
# @Author:lovemefan
# @File:weiboListener.py
# @Software:PyCharm

import pymysql
import time
# 打开数据库连接
from 微博爬虫 import sendEmail

db = pymysql.connect("ip", "账号", "密码", "weibo", charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()

def getCount():
    sql = "select getcount()"
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    item_count = results[0][0];
    return item_count


def sendMessage(text):
    sendEmail.sendmail("女神微博更新了o(*￣▽￣*)ブ",text)


if __name__ == '__main__':
    count = getCount()
    i = 0
    while True :
        # temp = getCount()
        temp = 0
        if temp != count:
            text = "更新%d条微博\n" % (temp - count)
            # get_top_info 为一个获得前五条数据的视图
            sql = "select created_at,source,scheme,text FROM get_top_info"
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for t in results:
                text = text + t[0] + "\n" + t[1] + "\n" + t[2] + "\n" + t[3] +"\n\n"
            print(text)
            sendMessage(text)
            count = temp
        print("当前%d次循环"%i)
        i = i + 1
        time.sleep(20)




