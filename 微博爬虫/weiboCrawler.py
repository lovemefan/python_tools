# -*- codeing: utf-8 -*-
# @Time:2018/5/28 14:31
# @Author:lovemefan
# @File:抓取女神微博动态保存到数据库.py
# @Software:PyCharm
#
#原始URL:https://m.weibo.cn/p/1005055629915400
import requests
import json
import pymysql
# 打开数据库连接
db = pymysql.connect("123.207.13.68", "li", "123456", "weibo", charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()
url="https://m.weibo.cn/api/container/getIndex"
page = 1
sum = 0
for k in range(35):
    # 用户的uid,containerid,以及页数.每页最多为十条记录
    payload={'type':'uid','value':'5629915400','containerid':'1076035629915400','page': '%d'%page}
    r=requests.post(url,data=payload)
    raw_text=r.text
    d=json.loads(raw_text)
    try:
        for i in range(10):
            print("第%d页第%d条"% (page,i))
            print(d["data"]["cards"])
            itemid = str(d["data"]["cards"][i]["itemid"])
            scheme = str(d["data"]["cards"][i]["scheme"])
            id = str(d["data"]["cards"][i]["mblog"]["id"])
            create_at = str(d["data"]["cards"][i]["mblog"]["created_at"])
            #将内容中的单引号换成双引号,否则插入数据库中会报错
            text = str(d["data"]["cards"][i]["mblog"]["text"]).replace("'","\"")
            source = str(d["data"]["cards"][i]["mblog"]["source"])
            user_id = str(d["data"]["cards"][i]["mblog"]["user"]["id"])
            # sql插入语句
            sql = "insert ignore into mblog(itemid,scheme,id,created_at,text,source,user_id) VALUES('%s','%s','%s','%s','%s','%s','%s')" % (itemid,scheme,id,create_at,text,source,user_id)
            print(sql)
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
            sum = sum + 1
    except IndexError:
        # 但记录不满10条的时候,捕获list越界异常,自动跳过
        pass

    page = page + 1
    print("第%d页执行成功"%page)
        # print(["text"])
db.close()
print("一共插入了%d的条记录"% sum)