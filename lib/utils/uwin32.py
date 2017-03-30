# -*- coding: utf-8 -*-

import win32clipboard as w
import win32con

def getClipboard():
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return d

def setClipboard(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_TEXT, aString)
    w.CloseClipboard()


#重写cmd输出的控制台,in main.py
#if sys.stdout.encoding == 'cp936':  
#    sys.stdout = UnicodeStreamFilter(sys.stdout)  
class UnicodeStreamFilter:  
    def __init__(self, target):  
        self.target = target  
        self.encoding = 'utf-8'  
        self.errors = 'replace'  
        self.encode_to = self.target.encoding  
    def write(self, s):  
        if type(s) == str:  
            s = s.decode("utf-8")  
        s = s.encode(self.encode_to, self.errors).decode(self.encode_to)  
        self.target.write(s)  