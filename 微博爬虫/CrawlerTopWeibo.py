# -*- codeing: utf-8 -*-
# @Time:2018/5/29 23:38
# @Author:lovemefan
# @File:CrawlerTopWeibo.py
# @Software:PyCharm
import requests
import json
import pymysql
# 打开数据库连接
import time
from email.mime.text import MIMEText
import smtplib

mailto_list = '450489712@qq.com'
mail_host = 'smtp.aliyun.com'
mail_user = 'xxxxxx.com'
mail_pass = 'xxxxxxxx'

def sendmail(conent):
    msg = MIMEText(conent, _subtype='html', _charset='utf-8')
    msg['Subject'] ="你的小可爱更新微博了"
    msg['From'] = 'python 提醒'
    msg['To'] = mailto_list
    print(mailto_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host, 25)
        s.login(mail_user, mail_pass)
        s.sendmail(mail_user, mailto_list, msg.as_string())
        s.close()
        return True
    except Exception as e:
        print(str(e))
        return False

if __name__ == '__main__':

    while True:
        try:
			db = pymysql.connect("123.207.13.68", "lovemefan", "Nchu19970208", "weibo", charset='utf8')
			url = "https://m.weibo.cn/api/container/getIndex"
			payload = {'type': 'uid', 'value': '5629915400', 'containerid': '1076035629915400'}
			# 使用cursor()方法获取操作游标
			cursor = db.cursor()
			r=requests.post(url,data=payload)
			raw_text=r.text
			d=json.loads(raw_text)
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
                    print("没有新动态")
        except :
            print("错误")
            pass
        cursor.close()
        db.close()
        time.sleep(5)