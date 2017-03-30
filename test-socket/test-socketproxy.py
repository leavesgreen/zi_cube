# -*- coding: utf-8 -*-
#!/usr/bin/python

import socket

apa_addr=('www.baidu.com',80) #原服务器;地址,但是在一般的代理中,如何得知原服务器地址呢? 对于http请求而言,可以解析头中的Host得到;但对于其他的tcp连接呢?
ser_addr=('127.0.0.1',8080)

apa =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ser =socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ser.bind(ser_addr)
ser.listen(5)
poll=[]

while True:
    con,addr=ser.accept()

    print addr
    print con

    poll.append(con)

    while len(poll):
        c=poll.pop(0)
        buf = c.recv(1024)

        print len(buf)

        if not buf:
            continue
        apa.connect(apa_addr)
        apa.send(buf)
        data = apa.recv(1024)
        c.send(data)
        c.close()
        apa.close()
