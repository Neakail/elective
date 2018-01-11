# -*- coding:utf-8 -*-

import requests
import multiprocessing
import gevent
import pytesseract
from  PIL import Image
import time
from gevent import monkey
monkey.patch_all()

classes = [
    'http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id=201720182012425'
]

def worker():
    req = requests.session()
    while True:
        try:
            while True:
                picture = req.get('http://jxgl.gdufs.edu.cn/jsxsd/verifycode.servlet').content
                with open('1', 'wb') as tupian:
                    tupian.write(picture)
                image = Image.open('1')
                vcode = pytesseract.image_to_string(image=image)
                print vcode
                data = {'USERNAME': '', 'PASSWORD': '', 'RANDOMCODE': vcode}
                b = req.post('http://jxgl.gdufs.edu.cn/jsxsd/xk/LoginToXkLdap', data=data)
                content = b.text.encode('utf-8')
                content.replace('/', '')
                if "验证码错误" in content:
                    print "验证码错误"
                else:
                    print "登录成功"
                    break
            c = req.get('http://jxgl.gdufs.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=80B88878FACB4DCA9278641DA6215189')
            content = c.text
            if u"当前未开放选课，具体请查看学校选课通知！" in content:
                print "当前未开放选课，具体请查看学校选课通知！"
                time.sleep(600)
                continue
            while True:
                flag = 0
                for each in classes:
                    pass
                    print req.get(each).text
                    if u"其他地方" in req.get(each).text:
                        flag = 1
                if flag == 1:
                    break
            time.sleep(3)
            continue
        except:
            time.sleep(3)
            continue


def gevent_requests():
    jobs = [gevent.spawn(worker) for i in range(16)]
    gevent.joinall(jobs)


def multi():
    pross = [multiprocessing.Process(target=worker) for i in range(1)]
    for i in pross:
        i.start()

    for i in pross:
        i.join()

if __name__ == '__main__':
    multi()
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
