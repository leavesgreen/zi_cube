# -*- coding: utf-8 -*-
#!/usr/bin/python

import os,time,signal

def chldhandler(sigum,stackframe):
    #signal handler,runs on the parent and is called whenever a child terminates. or other signal?
    while 1:
        try:
            result=os.waitpid(-1,os.WNOHANG) #-1,意思是等待所有已经终止的子进程; 第二个参数,如果没有已中止,立刻返回; 如果有子进程等待,返回进程pid,和退出信息; 使用wait,waitpid,来搜集终止进程,称为收割(reaping)
        except:
            break
        print 'Reaped child process %d' % result[0]

def reap_loop():
    while 1:
        try:
            result=os.waitpid(-1,os.WHOHANG)
        except:
            break
        print 'reaped child process %d' % result[0]


def reap_by_parent_loop(): #父进程相当于毛线都不干,只负责收割子进程;
    print 'Before the fork,my pid is ',os.getpid()

    pid =os.fork()
    if pid:
        print 'hello from the parent. the child will be pid %d' %pid
        print 'parent sleeping 60 seconds...'
        time.sleep(60)
        print 'parent sleep done.'
        reap_loop() #父进程开始毛线都不做,收割;
        print 'parent sleeping 60 seconds...'
        time.sleep(60)
        print 'parent sleep done.'
    else:
        print 'child sleeping 5 seconds.'
        time.sleep(5)
        print 'child terminating...'


def reap_by_signal(): #父进程等子进程歇菜的通知;
    signal.signal(signal.SIGCHLD,chldhandler)

    print 'Before the fork,my pid is ',os.getpid()

    pid =os.fork()
    if pid:
        print 'hello from the parent. the child will be pid %d' %pid
        print 'sleep 20 seconds...'
        time.sleep(20)
        print 'sleep done.'
    else:
        print 'child sleeping 5 seconds.'
        time.sleep(5)


if __name__=='__main__':
    reap_by_signal()
