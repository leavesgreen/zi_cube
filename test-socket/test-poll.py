# -*- coding: utf-8 -*-
#!/usr/bin/python

import socket,traceback,os,sys,select

class stateclass:
    stdmask = select.POLLERR |select.POLLHUP |select.POLLNVAL

    def __init__(self,mastersock):
        self.p=select.poll()
        self.mastersock = mastersock
        self.watchread(mastersock)
        self.buffers={}
        self.sockets={mastersock.fileno():mastersock}

    def fd2socket(self,fd):
        return self.sockets[fd]

    def watchread(self,fd):
        self.p.register(fd,select.POLLIN|self.stdmask)

    def watchwrite(self,fd):
        self.p.register(fd,select.POLLOUT|self.stdmask)

    def watchboth(self,fd):
        self.p.register(fd,select.POLLIN|select.POLLOUT|self.stdmask)

    def downwatch(self,fd):
        self.p.unregister(fd)

    def newconn(self,sock):
        fd=sock.fileno()
        self.watchboth(fd)
        self.buffers[fd] = 'welcome to the echo server, %s \n' % \
            str(sock.getpeername())
        self.sockets[fd] = sock

    def readevent(self,fd):
        try:
            self.buffers[fd]+= self.fd2socket(fd).recv(4096)
        except:
            self.closeout(fd)

        #这是每一次操作完之后都要重新注册?
        self.watchboth(fd)

    def writeevent(self,fd):

        if not  len(self.buffers[fd]):
            self.watchread(fd)
            return
        try:
            byteswritten = self.fd2socket(fd).send(self.buffers[fd]);
        except:
            self.closeout(fd)

        #delete the text sent from buffer.
        self.buffers[fd] = self.buffers[fd][byteswritten:]

        if not len(self.buffers[fd]):
            self.watchread(fd)

    def errorevent(self,fd):
        self.closeout(fd)

    def closeout(self,fd):
        self.downwatch(fd)
        try:
            self.fd2socket(fd).close()
        except:
            pass
        del self.buffers[fd]
        del self.sockets[fd]

    def loop(self):
        #main loop
        while 1:
            result = self.p.poll()
            for fd,event in result:
                if fd==self.mastersock.fileno() and event ==select.POLLIN:
                    try:
                        newsock,addr = self.fd2socket(fd).accept()
                        newsock.setblocking(0)
                        print 'got connection from ' , newsock.getpeername()
                        self.newconn(newsock)
                    except Exception as e:
                        raise
                elif event ==select.POLLIN:
                    self.readevent(fd)
                elif event ==select.POLLOUT: #什么时候通知的?
                    self.writeevent(fd)
                else:
                    self.errorevent(fd)

if __name__=='__main__':

        host=''
        port=51423

        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((host,port))
        s.listen(1)
        s.setblocking(0)

        state = stateclass(s)
        state.loop()
