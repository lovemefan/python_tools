# -*- codeing: utf-8 -*-
# @Time:2018/5/29 17:39
# @Author:lovemefan
# @File:sendEmail.py
# @Software:PyCharm

import configparser
import os
from email.mime.text import MIMEText
import smtplib

mailto_list = '450489712@qq.com'
mail_host = 'smtp.aliyun.com'
mail_user = 'XXXXXX@aliyun.com'
mail_pass = 'XXXXXXXX'

def sendmail(conent):
    msg = MIMEText(conent, _subtype='html', _charset='utf-8')
    msg['Subject'] ="你有一封情书待查收"
    msg['From'] = '你的小可爱'
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



sendmail('o(*￣▽￣*)ブ💗')