# -*- coding:utf-8 -*-

import requests
import multiprocessing
import gevent
import pytesseract
from  PIL import Image
import time
from gevent import monkey
from lxml import etree
import json
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
            url = selector.xpath("//table//tr//td//a/@href")[0]
            print url
            break
    return url

def click(url):
    req.get('http://jxgl.gdufs.edu.cn' + url)
    kecheng = {}
    list_ = req.get('http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/xsxkXxxk').text
    print list_
    list_ = json.loads(list_)
    for i in list_["aaData"]:
        print i
        kecheng[i['kcmc']] = i['jx0404id']
    for i in kecheng:
        print i,kecheng[i]
    lesson_list = raw_input('请输入你要选择的课程，不同课程请以-隔开:\n')
    lesson_list = lesson_list.split('-')
    processed_lesson_list = []
    base_url = 'http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id='
    for lesson in lesson_list:
        processed_lesson_list.append(base_url+lesson)
        print base_url+lesson

    while True:
        for i in processed_lesson_list:
            text = req.get(i).text
            print text


def gevent_requests():
    jobs = [gevent.spawn(worker) for i in range(16)]
    gevent.joinall(jobs)


def multi(url):
    pross = [multiprocessing.Process(target=click,args=(url,)) for i in range(2)]
    for i in pross:
        i.start()

    for i in pross:
        i.join()

def main(username,password):
    url = worker(username,password)
    click(url)

if __name__ == '__main__':
    username  = ""
    password = ""
    main(username,password)
