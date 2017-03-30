#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'iris'
import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient
import functools
def bbb():

    return "cccccccccccccccccccccccccccccccccccc"
def aaa():

    return "dddddddddddddddddddddddddddddddddddd"

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
        callback(gen,bbb())
    return wrapper

@sync
def fetch():
    response = yield aaa
    print '1'
    print response
    print '2'

if __name__=="__main__":
    k=0

    while k <5:
        fetch()
        k+=1

    #tornado.ioloop.IOLoop.instance().start()
