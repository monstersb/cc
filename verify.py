#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import threadpool
import socket
import requests
import time
import random

class CC(object):
    def __init__(self):
        self.importproxy()

    def importproxy(self):
        self.proxy = []
        for i in self.readfile('proxy.txt').split():
            if i.strip() == '':
                continue
            self.proxy.append(i)#{'http':'http://{0}/'.format(i.strip())})

    def readfile(self, fname):
        with open(fname, 'r') as f:
            return f.read()

    def attack(self, x):
        for i in range(3):
            try:
                proxy = {'http':'http://{0}/'.format(x.strip())}
                r = requests.get('http://qt.gtimg.cn', timeout=3, proxies=proxy)
                if r.status_code == 400 and r.content == 'ERROR(400,unknown request)':
                    print x
                    return
            except Exception:
                continue

    def run(self):
        pool = threadpool.ThreadPool(10)
        reqs = threadpool.makeRequests(self.attack, self.proxy)
        [pool.putRequest(req) for req in reqs]
        pool.wait()


if __name__ == '__main__':
    cc = CC()
    cc.run()
    time.sleep(0.5)
    exit()
