# -*- codeing: utf-8 -*-
# @Time:2018/4/1 11:13
# @Author:lovemefan
# @File:网易云签到.py
# @Software:PyCharm
# coding:utf-8
import datetime

import requests
import os
import smtplib
from email.mime.text import MIMEText

import time

'''
netbase sign
type=1 web sign
type=0 phone sign
os travis-ci profile
return value
code：200 Sign Success
code: -2 Repeat sign
'''

mailto_list = '15201430@stu.nchu.edu.cn'
mail_host = 'smtp.163.com'
mail_user = '18679128652@163.com'
mail_pass = 'Nchu19970208'
curTime = ''



def netbaseqiandao(typeid):
    cookies = {'MUSIC_U': "4a86c3b3c2932e33b13099a4a830a0fc19cd98a376929b237c96b01ebfb2741cfea42ded665577e8b1caf26b6d7923a241049cea1c6bb9b6"}
    url = 'http://music.163.com/api/point/dailyTask?type=%s&csrf_token=1c026fa76277d4f44749025932ea47f0' % typeid
    headers = {
        'Referer': 'http://music.163.com/discover',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.30 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*'
    }
    res = requests.post(url, cookies=cookies, headers=headers)
    curTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n")
    sendmail(curTime + res.text)
    return res.text


def sendmail(conent):
    if '200' in conent or '-2' in conent:
        print(conent)
    else:
        # 签到失败时邮件通知
        msg = MIMEText(conent, _subtype='html', _charset='utf-8')
        msg['Subject'] = curTime + '网易云签到通知'
        msg['From'] = mail_user
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


def sign():
    netbaseqiandao(0)
    netbaseqiandao(1)


def signEveryday(shed_time):
    flag = 0
    while True:
        now = datetime.datetime.now()
        if now.day == shed_time.day:
            if now.hour == shed_time.hour and flag == 0:
                sign()
                flag = 1
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n") + "已签到")
            else:
                time.sleep(600);
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
                    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n") + "昨日签到失败")
            else:
                time.sleep(3600)



if __name__ == '__main__':
    now = datetime.datetime.now()
    shed_time = datetime.datetime(now.year,now.month,now.day,6,0,0) + datetime.timedelta(days=1)
    # 当前立即签到
    sign()
    # 从次日6点定时签到
    signEveryday(shed_time)