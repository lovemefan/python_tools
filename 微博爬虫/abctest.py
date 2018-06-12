# -*- codeing: utf-8 -*-
# @Time:2018/6/7 19:15
# @Author:lovemefan
# @File:abctest.py
# @Software:PyCharm
# -*- codeing: utf-8 -*-
# @Time:2018/6/7 19:10
# @Author:lovemefan
# @File:test.py
# @Software:PyCharm
import json

import requests

url="https://m.weibo.cn/api/container/getIndex"
payload={'type':'uid','value':'5629915400','containerid':'1076035629915400'}


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
    print(id)