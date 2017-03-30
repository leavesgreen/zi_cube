#!/usr/bin/env python  #define run direct on linux.unix.mac
# -*- coding: utf-8 -*-


'test udp'

__author__ = 'iris'

import socket
import time,threading

#server
if __name__ =="__main1__":
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #数据报,与tcp的流不同;
    s.bind(('127.0.0.1',9999)) #可以与TCP使用相同的端口,也可以使用多线程
    print 'Bind UDP on 9999...'
    while True:
        #接受数据
        data,addr = s.recvfrom(1024)
        print 'Received from %s:%s.' % addr
        s.sendto('Hello,%s!' %data,addr)

#client
if __name__ =="__main2__":
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    for data in ['1111','2222','3333']:
        s.sendto(data,('127.0.0.1',9999))
        print s.recv(1024)
    s.close()