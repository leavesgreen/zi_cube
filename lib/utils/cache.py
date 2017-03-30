# coding=utf-8
# author: tonyseek
import time
from datetime import datetime,timedelta
import os,sys


class miniCache(object):

    __max_entry = 3000
    __cache = {};

    def clear(self):
        for key, value in miniCache.__cache.iteritems():
            expiry = value[1]
            if expiry and datetime.now() > expiry:
                del miniCache.__cache[key]

    def __init__(self):
        pass;

    def values(self):
        return (x[0] for x in miniCache.__cache.values());


    @classmethod
    def getinstance(cls):
        if not hasattr(cls,'_instance'):
            cls._instance = miniCache();
        return cls._instance;

    def flush_all(self):
        miniCache.__cache = {}

    def set(self, key, value, expiretime):
        if not expiretime:
            expiretime = datetime.now()

        #miniCache.__cache[key] = (value, time.time() + seconds if seconds else 0)
        if len(miniCache.__cache)>=miniCache.__max_entry:
            self.clear()

        miniCache.__cache[key] = (value, expiretime)
        
    def get(self, key):
        value = miniCache.__cache.get(key,None)

        
        if value:
            expiry = value[1]
            if expiry and  datetime.now() > expiry:
                del miniCache.__cache[key]
                return None
            else:
                return value[0]

        else:
            return None


    def delete(self, key):
        if key in miniCache.__cache:
            del miniCache.__cache[key]
        return None


if __name__== '__main__':
    a = miniCache.getinstance();
    a.set('001','aaa',datetime.now()+timedelta(milliseconds=100));
    a.set('002','bbb',datetime.now()+timedelta(milliseconds=100));

    print a.get('002');