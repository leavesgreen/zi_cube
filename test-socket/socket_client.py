# -*- coding: utf-8 -*-
#!/usr/bin/python

import socket,sys,struct,time

def test_tcp_client():
    print 'creating socket'
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print 'done'

    print 'connecting to remote host...'
    port = socket.getservbyname('http','tcp')
    s.connect(('www.163.com',port))
    print 'done'

    print 'connect from ', s.getsockname()
    print 'connect to',s.getpeername()

def test_tcp_client_by_bigbuffer():
    hostname='localhost'
    port=51423




    host=socket.gethostbyname(hostname) #DNS
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #UDP
    s.connect((host,port))

    data = 'x'*10485760 #还能这么玩
    bytes_written =0
    while bytes_written<len(data):
        startpos=bytes_written
        endpos = min(bytes_written+1024,len(data))
        bytes_written +=s.send(data[startpos:endpos])
        sys.stdout.write('wrote %d bytes \r' %bytes_written) #可以原位置刷新,帅;
        sys.stdout.flush()

    s.shutdown(1)
    print 'All data sent'
    while 1:
        buf = s.recv(1024)
        print buf
        if not len(buf):
            break
        sys.stdout.write(buf)



def test_udp_client():
    hostname='time.nist.gov'
    port=37

    host=socket.gethostbyname(hostname) #DNS
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #UDP
    s.sendto('',(host,port))

    print 'looking for replies,press ctrl+C to stop'
    buf=s.recvfrom(2038)[0] #recvfrom 返回一个tuple,(实际接受数据,(发送数据的机器地址,端口))
    print buf
    if len(buf)!=4:
        print 'wrong-sized reply %d : %s' % (len(buf),buf)
        sys.exit(1)

    secs = struct.unpack("!I",buf)[0]
    secs -= 2208988800
    print time.ctime(int(secs))


def test_udp_client_local():
    hostname='localhost'
    port=51423

    host=socket.gethostbyname(hostname) #DNS
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #UDP
    s.sendto('fuck all those team killers',(host,port))

    print 'looking for replies,press ctrl+C to stop'
    buf=s.recvfrom(2038)[0] #recvfrom 返回一个tuple,(实际接受数据,(发送数据的机器地址,端口))

    print buf
    #if len(buf)!=4:
    #    print 'wrong-sized reply %d : %s' % (len(buf),buf)
    #    sys.exit(1)

    #secs = struct.unpack("!I",buf)[0]
    #secs -= 2208988800
    #print time.ctime(int(secs))

def test_broadcast_client():
    host=''
    port=51423

    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    s.bind((host,port))

    while 1:
        try:
            message,address=s.recvfrom(8192)
            print 'got data from ',address

            s.sendto('i am here',address)
        except (KeyboardInterrupt,SystemExit):
            raise
        except:
            traceback.print_exec()




if __name__=='__main__':
    #test_tcp_client()
    #test_udp_client()
    test_broadcast_client()
