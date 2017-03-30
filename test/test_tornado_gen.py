#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.ioloop
from tornado.gen import coroutine
from tornado.concurrent import Future
import functools


def callback(a, b):
    print("calculating the sum of %d+%d:"%(a,b))
    ft1.set_result(a+b)



def ayncFunc(a,b,callback):



@coroutine
def asyn_sum(a, b):
    print("begin calculate:sum %d+%d"%(a,b))
    future = Future()
    tornado.ioloop.IOLoop.instance().add_callback(callback, a, b,future)

    result = yield future

    print("after yielded")
    print("the %d+%d=%d"%(a, b, result))

def main():
    asyn_sum(2,3)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
