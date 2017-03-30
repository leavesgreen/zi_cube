#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'iris'
import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient
import functools

def task(fun, url):
    return functools.partial(fun, url)

def callback(gen, response):
    try:
        print 'callback:', response
        gen.send(response)
    except StopIteration:
        pass

def sync(func):
    def wrapper():
        gen = func()

        f = gen.next()
        print 'aa', f, gen
        f(functools.partial(callback, gen))
    return wrapper

@sync
def fetch():
    response = yield task(AsyncHTTPClient().fetch, 'http://www.163.com/')
    print '1'
    print response
    print '2'

if __name__=="__main__":
    print 'aaaaaaaaa'
    fetch()

    print 3
    #tornado.ioloop.IOLoop.instance().start()
