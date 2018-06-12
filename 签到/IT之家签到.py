# -*- codeing: utf-8 -*-
# @Time:2018/4/1 15:58
# @Author:lovemefan
# @File:IT之家签到.py
# @Software:PyCharm

#it之家只需要提交一个get请求即可完成签到
import datetime
from time import sleep

import requests
def sign():
    # 所需的url,通过手机抓包得到
    url = 'https://my.ruanmei.com/api/usersign/sign?userhash=f1772763bfced4b31e6f78afef7a4591ced04c14164cd816c7c9fb2edaf0b53e462454006f98d0c31eb5f948836ee6ac1d35e0d8c3adc149&type=0&appver=600'
    response = requests.get(url)
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n") + response.text + '\n\n')

def signEveryday(shed_time):
    while True:
        flag = 0
        now = datetime.datetime.now()
        if now.day == shed_time.day:
            if now.hour == shed_time.hour and flag == 0:
                sign()
                flag = 1
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n")+"已签到")
            else:
                sleep(600);
        else:
            # 当前时间与要签到时间不一致


            if now.day >= shed_time.day:
                # 昨日已签到
                if flag == 1:
                    shed_time = shed_time + datetime.timedelta(days=1)
                    flag = 0
                else:
                    # 昨日签到失败
                    # 一定要休眠,否则将消耗大量cpu资源
                    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n")+"昨日签到失败")
            else:
                sleep(3600)

if __name__ == '__main__':
    now = datetime.datetime.now()
    shed_time = datetime.datetime(now.year, now.month, now.day, 6, 0, 0) + datetime.timedelta(days=1)
    # 当前立即签到
    sign()
    # 次日起没天6点签到
    signEveryday(shed_time)