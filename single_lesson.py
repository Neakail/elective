# -*- coding:utf-8 -*-

import requests
import multiprocessing
import gevent
import pytesseract
import time
from  PIL import Image
from gevent import monkey
from lxml import etree
monkey.patch_all()

req = requests.session()

def worker(username,password):
    url = ''
    while True:
        picture = req.get('http://jxgl.gdufs.edu.cn/jsxsd/verifycode.servlet').content
        with open(username, 'wb') as tupian:
            tupian.write(picture)
        image = Image.open(username)
        vcode = pytesseract.image_to_string(image=image)
        print vcode
        data = {'USERNAME': username, 'PASSWORD': password, 'RANDOMCODE': vcode}
        b = req.post('http://jxgl.gdufs.edu.cn/jsxsd/xk/LoginToXkLdap', data=data)
        content = b.text.encode('utf-8')
        content.replace('/', '')
        if "验证码错误" in content:
            print "验证码错误"
        else:
            print "登录成功"
            c = req.get('http://jxgl.gdufs.edu.cn/jsxsd/xsxk/xklc_list')
            content = c.text.encode('utf-8')
            selector = etree.HTML(content)
            url = "/jsxsd/xsxk/xsxk_index?jx0502zbid=80B88878FACB4DCA9278641DA6215189"
            print url
            break
    return url

def click(url,kecheng_url):
    req.get('http://jxgl.gdufs.edu.cn' + url)
    while True:
        text = req.get(kecheng_url).text
        print text
	time.sleep(1)

def gevent_requests():
   jobs = [gevent.spawn(worker) for i in range(16)]
   gevent.joinall(jobs)	


def multi(url):
    pross = [multiprocessing.Process(target=click,args=(url,)) for i in range(2)]
    for i in pross:
        i.start()

    for i in pross:
        i.join()

def main(username,password,kecheng_url):
    url = worker(username, password)
    click(url,kecheng_url)

if __name__ == '__main__':
    username = ''
    password = ''
    kecheng_url = ''
    main(username,password,kecheng_url)
