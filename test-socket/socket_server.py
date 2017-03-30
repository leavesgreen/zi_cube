# -*- coding: utf-8 -*-
#!/usr/bin/python

import socket,sys,struct,time,traceback


def test_tcp_server():
    host=''
    port=51423

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #(level,optname,value),通常是SOL_SOCKET,
    s.bind((host,port)) #host为空,表示绑定所有的接口和地址;
    print 'waiting for connections....'
    s.listen(2) #默认是5,表示有多少个未读的连接在队列中等待;
    while 1:
        clientsock,clientaddr = s.accept() #会阻塞
        print 'got connection from ',clientsock.getpeername()
        clientsock.close()

def test_udp_server():
    host=''
    port=51423

    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #(level,optname,value),通常是SOL_SOCKET,
    s.bind((host,port)) #host为空,表示绑定所有的接口和地址;
    print 'waiting for connections....'
    #s.listen(2) # 注意,没有监听;
    while 1:
        try:
            message,address = s.recvfrom(8192) #also阻塞?
            print 'got data from ',address
            s.sendto(message,address)
        except KeyboardInterrupt:
            raise
        except:
            traceback.print_exec()
            continue

def test_tcp_server_by_bigbuffer():
    host='192.168.10.106'
    port=51423

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #(level,optname,value),通常是SOL_SOCKET,
    s.bind((host,port)) #host为空,表示绑定所有的接口和地址;
    print 'waiting for connections....'
    s.listen(2) #默认是5,表示有多少个未读的连接在队列中等待;

    alldata = ''
    while 1:
        clientsock,clientaddr = s.accept() #会阻塞
        print 'got connection from ',clientsock.getpeername(), clientaddr
        while 1:
            data = clientsock.recv(4096)
            alldata+=data
            if not len(data):
                break
            #clientsock.sendall(data) #边读取边发送,会造成死锁,因为客户端一直在发送,发送完才接受; 客户端要么读/写,读/写,或者使用多线程;
        #print alldata
        clientsock.sendall(alldata)
        clientsock.close()


def test_broadcast_server():
    #host=''
    port=51423

    dest=('<broadcast>',port)
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    s.sendto('hello all buddys',dest)

    print 'looking for replies; press ctrl+c to stop.'
    while 1:
        (buf,address) = s.recvfrom(2048)
        if not len(buf):
            break
        print 'received from %s:%s' % (address,buf)


if __name__=='__main__':
    #test_tcp_client()
    #test_udp_client()
    #
    #test_broadcast_server()
    test_tcp_server_by_bigbuffer()
