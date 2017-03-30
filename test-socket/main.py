#coding=utf8

import socket
import sys
import argparse


from binascii import hexlify  #for ascii and 二进制转换;

def print_machine_info():

    host_name=socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    print "Host name: %s" % host_name
    print 'Ip Address: %s' % ip_address


def get_remote_machine_info():
    remote_host = 'www.baidu.com'
    try:
        print 'Ip Address: %s' % socket.gethostbyname(remote_host)
    except socket.error,err_msg:
        print '%s : %s ' %(remote_host,err_msg)


def convert_ip4_address():
    for ip_addr in ['127.0.0.1','192.168.1.1']:
        packed_ip_addr=socket.inet_aton(ip_addr) #转为32位2进制格式;
        unpacked_ip_addr=socket.inet_ntoa(packed_ip_addr)
        print 'IP Adress: %s =>Packed: %s ,Unpacked: %s ' % (ip_addr,hexlify(packed_ip_addr),unpacked_ip_addr)


#根据端口和协议找到service名字;
def find_service_name(): 
    protocolname='tcp'
    for port in [80,25]:
        print 'Port:%s =>service name :%s ' %(port,socket.getservbyport(port,protocolname))
        print 'Port:%s => service name :%s ' %(53,socket.getservbyport(53,'udp'))


#将数据,在网络字节序和主机字节序之间转换
def convert_integer():
    data =1234
    print 'Original: %s=> long host byte order: %s, Network byte order: %s' %(data,socket.ntohl(data),socket.htonl(data)) #32bit, HTONL
    print 'Original: %s=> long host byte order: %s, Network byte order: %s' %(data,socket.ntohs(data),socket.htons(data)) #16bit


#套接字的默认超时时间

def test_socket_timeout():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #AF_INET6(ip4,ip6); SOCK_STREAM,套接字类型;
    print 'Default socket timeout : %s ' % s.gettimeout()
    s.settimeout(100) #修改超时时间
    print 'Current socket timeout : %s ' % s.gettimeout()

#处理socket 错误

def error_handler():
    parser = argparse.ArgumentParser(description='Socket Error Examples')
    parser.add_argument('--host',action='store',dest='host',required=False)
    parser.add_argument('--port',action='store',dest='port',type=int,required=False)
    parser.add_argument('--file',action='store',dest='file',required=False)

    given_args=parser.parse_args()
    host=given_args.host
    port = given_args.port
    filename=given_args.file

    #first try-except block --create socket
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #
    except socket.error,e:
        print 'Error creating socket: %s' % e
        sys.exit(1)


    #second try-except block ,coonect to given host/port
    try:
        s.connect((host,port))
    except socket.gaierror,e:
        print 'Address-related error connecting to server %s' % e  #地址相关的错误
        sys.exit(1)
    except socket.error,e:
        print "Connection error: %s "%e
        sys.exit(1)

    #third,try except block, --sending data
    try:
        s.sendall("Get %s HTTP/1.0 \r\n\r\n" % filename)
    except socket.error,e:
        print "Error sending data:%s" % e
        sys.exit(1)

    while 1:
        try:
            buf = s.recv(2048)
        except socket.error,e:
            print "Error receiving data: %s" % e
            sys.exit(1)
        if not len(buf):
            break
        sys.stdout.write(buf)


SEND_BUF_SIZE=4096
RECV_BUF_SIZE=4096

def modify_buff_size():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    bufsize=sock.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF) #???参数的意义
    print 'Buffer size [Before]: %s' % bufsize

    sock.setsockopt(socket.SOL_TCP,socket.TCP_NODELAY,1)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,SEND_BUF_SIZE)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,RECV_BUF_SIZE)

    bufsize = sock.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF) #get socket properties.
    print 'Buffer size [After]: %s' % bufsize



if __name__=='__main__':
    '''
    print_machine_info()
    get_remote_machine_info()
    convert_ip4_address()
    find_service_name()
    convert_integer()

    test_socket_timeout()
    '''

    #error_handler()

    modify_buff_size()