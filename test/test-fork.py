# -*- coding: utf-8 -*-
#!/usr/bin/python

import os,time

print 'beforre the fork, my pid is',os.getpid()

if os.fork():
    print 'hello from the parent. my pid is ', os.getpid()
else:
    print 'hello from the child.my pid is ',os.getpid()

time.sleep(1)
print 'hello from both of us.'
