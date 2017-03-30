#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
  
import os  
  
class IOLoop(object):  
    @classmethod  
    def instance(cls):  
        if not hasattr(cls, "_instance"):  
            cls._instance = cls()  
        return cls._instance  
 
    @classmethod  
    def initialized(cls):  
        """Returns true if the singleton instance has been created."""  
        return hasattr(cls, "_instance")  
  
    def service(self):  
      print 'Hello,World'  
  
print IOLoop.initialized(),  
ioloop = IOLoop.instance()  
ioloop.service()  
  
if os.fork() == 0:  
  print IOLoop.initialized(),  
  ioloop = IOLoop.instance()  
  ioloop.service()  

