#!/usr/bin/env python  #define run direct on linux.unix.mac
# -*- coding: utf-8 -*-

#于客户端，要主动连接服务器的IP和指定端口，对于服务器，要首先监听指定端口，然后，对每一个新的连接，创建一个线程或进程来处理。通常，服务器程序会无限运行下去。

'test tcp'

__author__ = 'iris'

import socket
import time,threading

#client,test only receive and not send.
if __name__=="__main__":
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #ipv4
    s.connect(('127.0.0.1',9999))

    #接收欢迎消息
    print s.recv(2048) #1024含义?
    file = open('./aaaaaaaaaaaa.jpg','wb')

    data = s.recv(2048)
    i = 1
    while data:
        

        #print data
        #print 'end get:'+str(i)
        file.write(data)
        data = s.recv(2048)
        
        i+=1
    
    file.close()

    s.send('exit')
    print 'send exit.....'
    s.close()

if __name__=="__main3__":
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #ipv4
    s.connect(('127.0.0.1',9999))

    #接收欢迎消息
    print s.recv(1024) #1024含义?
    for data in ['1111','2222','3333']:
        #发送
        s.send(data)
        print s.recv(1024)
    s.send('exit')
    s.close()



#server,http的协议的,其格式必须符合要求;
if __name__=="__main2__":
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('0.0.0.0',9999))
    s.listen(5)  #最大数量
    print 'Waiting for connection...'
    while True:
        #接受新连接
        sock,addr = s.accept()
        #新线程,处理
        t = threading.Thread(target=tcplink,args=(sock,addr))
        t.start()

def tcplink(sock,addr):
    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data=='exit' or not data:
            break
        sock.send('Hello,%s!' % data)
        sock.close()
        print 'Connection from %s:%s closed.' % addr







