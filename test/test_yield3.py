#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'iris'
import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient
import functools

def yd1():
    print ' yd1.start...'
    t = yd2()
    #yield t.next();

    yield t.next()
    yield t.send('aaaaa')
    yield t.next();

def yd2():
    print ' yd2.start...'
    b= yield '03'
    print 'b:',b
    b =yield b
    print 'b:',b
    yield '05'


if __name__=="__main__":
    k=0
    a = yd1()
    while k <3:
        print a.next()
        k+=1

    #tornado.ioloop.IOLoop.instance().start()
