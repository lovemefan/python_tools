# -*- codeing: utf-8 -*-
# @Time:2018/2/8 10:28
# @Author:lovemefan
# @File:豆瓣模拟登录.py
# @Software:PyCharm
import requests
from PIL import Image
import pytesser3

def login():
    heads ={
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept - Language': 'zh - CN, zh;q = 0.8',
        'Cache - Control': 'max - age = 0',
        'Connection': 'keep - alive',
        'Content - Length': '75',
        'Content - Type': 'application / x - www - form - urlencoded',
        'Referer': 'https://www.douban.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    }
    # 获取验验证信息
    response = requests.get('https://www.douban.com/j/misc/captcha', headers=heads)
    result = response.json()
    captchaUrl = result['url']
    captchaToken = result['token']
    print(captchaToken)
    # 获取验证码图片
    response = requests.get('https:'+captchaUrl, headers=heads)
    codeimg = response.content
    fn = open('code.png','wb')
    fn.write(codeimg)
    fn.close()

    fn = open('code.png','rb')
    text = pytesser3.image_file_to_string(fn, graceful_errors=True)
    print(text)
    fn.close()

    data = {
        'source': 'index_nav',
        'redir':'https: // www.douban.com /',
        'form_email': '450489712@qq.com',
        'form_password': 'zlf19970208@',
        'captcha - id': captchaToken,
        'captcha - solution': input("请输入验证码:")
    }
    #登录
    url = 'https://www.douban.com/accounts/login'
    response = requests.post(url,data=data,headers=heads)
    if('lovemefan' in response.text):
        print('登录成功')
    else:
        print('登录失败')
def loginOut():
    url = 'https://www.douban.com/accounts/logout?source=main&ck=Yo1H'
    requests.get(url)

login()

# loginOut()