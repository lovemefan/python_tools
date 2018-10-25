# -*- codeing: utf-8 -*-
# @Time:2018/5/29 23:38
# @Author:lovemefan
# @File:CrawlerTopWeibo.py
# @Software:PyCharm
import datetime

import requests
import json
import pymysql
# 打开数据库连接
import time
from email.mime.text import MIMEText
import smtplib
import zmail

mailto_list = ['xxxxx2@qq.com','xxxxxxxx@outlook.com']
mail_host = 'smtp.163.com'
mail_user = '1xxxxxxxx2@163.com'
mail_pass = 'xxxxxxxxxxx'


def sendmail(conent):
    mail = {
        'subject': '小可爱更新微博了',  
        'content': conent,  
    }
    # 使用你的邮件账户名和密码登录服务器
    server = zmail.server(mail_user,mail_pass)
    # 发送邮件
    server.send_mail(mailto_list, mail)

def my_request(url,payload):
    try:
        return requests.post(url,data=payload)
    except Exception as e:
        print(e)
        return my_request

if __name__ == '__main__':

    while True:
        db = pymysql.connect("xxxxxxxxx", "xxxxxxx", "xxxxxxx", "xxxxxxxx", charset='utf8')
        url = "https://m.weibo.cn/api/container/getIndex"
        payload = {'type': 'uid', 'value': '562xxxxx00', 'containerid': '107xxxxxxxxx400'}
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        r=my_request(url,payload)
        raw_text=r.text
        try:
            d=json.loads(raw_text)
        except:
            print(raw_text)
            
        try:
            for i in range(5):
                itemid = str(d["data"]["cards"][i]["itemid"])
                scheme = str(d["data"]["cards"][i]["scheme"])
                id = str(d["data"]["cards"][i]["mblog"]["id"])
                create_at = str(d["data"]["cards"][i]["mblog"]["created_at"])
                # 将内容中的单引号换成双引号,否则插入数据库中会报错
                text = str(d["data"]["cards"][i]["mblog"]["text"]).replace("'", "\"")
                source = str(d["data"]["cards"][i]["mblog"]["source"])
                user_id = str(d["data"]["cards"][i]["mblog"]["user"]["id"])
                # 先查询数据库中是否存在
                sql = "select count(*) from mblog where id = '%s'" % id
                cursor.execute(sql)
                results = cursor.fetchall()
                if results[0][0] == 0:
                    # sql插入语句
                    sql = "insert ignore into mblog(itemid,scheme,id,created_at,text,source,user_id) VALUES('%s','%s','%s','%s','%s','%s','%s')" % (
                    itemid, scheme, id, create_at, text, source, user_id)
                    print(sql)
                    # 执行sql语句
                    cursor.execute(sql)
                    # 执行sql语句
                    db.commit()
                    # 发送邮件给我
                    context = '''微博链接: %s 
                     内容: %s ''' % (scheme,text)
                    sendmail(context)
                    print("已发送邮件")
                else:
                    # print(sql)
                    # print(text)
                    if i == 4:
                        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n")+"小公主可爱没有新动态")
        except :
            print("错误")
            pass
        cursor.close()
        db.close()
        time.sleep(10)