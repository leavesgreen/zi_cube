# -*- coding: utf-8 -*- 

import time,datetime
from dateutil import relativedelta
import ustr

#待处理
def is_date(str1):
    try:
        datetime.datetime.strptime(str1,'%Y-%m-%d')
        return true
    except Exception,e:
        return false

def date_to_str(d1,fmt='%Y-%m-%d %H:%M:%S'):

    str1 = "1900-01-01 00:00:00"
    try:
        return datetime.datetime.strftime(d1,fmt)
    except Exception,e:
        return str1

def date_to_str_s(d1,fmt='%Y-%m-%d'):

    str1 = "1900-01-01"
    try:
        return datetime.datetime.strftime(d1,fmt)
    except Exception,e:
        return str1

def str_to_date(str1,fmt='%Y-%m-%d %H:%M:%S'):

    try:        
        return datetime.datetime.strptime(str1,fmt)

    except Exception,e:
        return str_to_date_s(str1)
        

def str_to_date_s(str1,fmt='%Y-%m-%d'):

    try:
        return datetime.datetime.strptime(str1,fmt)
    except Exception,e:
        return datenull()

def date(d1):
    try:
        return datetime.datetime.strftime(d1,'%Y-%m-%d')
    except Exception,e:
        print e
        return datenull()

def day(d1):
    try:
        return ustr.atoi(datetime.datetime.strftime(d1,'%d'))
    except Exception,e:
        print e
        return 1

def year(d1):
    try:
        return ustr.atoi(datetime.datetime.strftime(d1,'%Y'))
    except Exception,e:
        print e
        return 1900

def month(d1):
    try:
        return ustr.atoi(datetime.datetime.strftime(d1,'%m'))
    except Exception,e:
        print e
        return 1

def datenull():
    return datetime.datetime.strptime("1900-01-01",'%Y-%m-%d')

def date_to_disp(dt):
    fmt='%Y-%m-%d %H:%M:%S'
    try:
        return datetime.datetime.strftime(dt,fmt)
    except Exception,e:
        return ""

def date_to_disp_s(dt):
    fmt='%Y-%m-%d'
    try:
        return datetime.datetime.strftime(dt,fmt)
    except Exception,e:
        return ""
def timestamp2disp(value):
    if value is None or value==0 or str(value)=='':
        return ''
        
    try:
       return date_to_disp(timestamp2datetime(value))
    except Exception,e:
        return ""

def timestamp2disp_s(value):

    if value is None or value==0 or str(value)=='':
        return ''

    try:
       return date_to_disp_s(timestamp2datetime(value))
    except Exception,e:
        return ""

 
def timestamp2datetime  (value):
    try:
        if value is None or value==0 or str(value)=='':
            return datenull()


        format = '%Y-%m-%d %H:%M:%S'
        # value为传入的值为时间戳(整形)，如：1332888820
        value = time.localtime(value)
        ## 经过localtime转换后变成
        ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
        # 最后再经过strftime函数转换为正常日期格式。
        dt = time.strftime(format, value)

        return str_to_date(dt)
    except Exception,e:
        return datenull()
 
def datetime2timestamp(dt):
    try:
        if not is_date(dt):
            return None
        #dt为字符串
        #中间过程，一般都需要将字符串转化为时间数组
        time.strptime(dt, '%Y-%m-%d %H:%M:%S')
        ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
        #将"2012-03-28 06:53:40"转化为时间戳
        s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
        return int(s)
    except Exception,e:
        return None


#timeSpan

'''
if  _now > _end_date+relativedelta.relativedelta(months=6):
                            #过期
                            _tmp["law_status"] = "3.4"
                        elif _now >_end_date and _now <=_end_date+relativedelta.relativedelta(months=6): #宽展
                            _tmp["law_status"] = "3.2"
                        elif _now >=_end_date+relativedelta.relativedelta(months=-6)  and _now <=_end_date:#续展
                            _tmp["law_status"] = "3.3"
                        #elif _now <_end_date+relativedelta.relativedelta(months=-6):
'''


class workDays():
    def __init__(self, start_date, end_date, days_off=None):
        """days_off:休息日,默认周六日, 以0(星期一)开始,到6(星期天)结束, 传入tupple
        没有包含法定节假日,
        """
        self.start_date = start_date
        self.end_date = end_date
        self.days_off = days_off
        if self.start_date > self.end_date:
            self.start_date,self.end_date = self.end_date, self.start_date
        if days_off is None:
            self.days_off = 5,6
        # 每周工作日列表
        self.days_work = [x for x in range(7) if x not in self.days_off]
 
    def workDays(self):
        """实现工作日的 iter, 从start_date 到 end_date , 如果在工作日内,yield 日期
        """
        # 还没排除法定节假日
        tag_date = self.start_date
        while True:
            if tag_date > self.end_date:
                break
            if tag_date.weekday() in self.days_work:
                yield tag_date
            tag_date += datetime.timedelta(days=1)
 
    def daysCount(self):
        """工作日统计,返回数字"""
        return len(list(self.workDays()))
 
    def weeksCount(self, day_start=0):
        """统计所有跨越的周数,返回数字
        默认周从星期一开始计算
        """
        day_nextweek = self.start_date
        while True:
            if day_nextweek.weekday() == day_start:
                break
            day_nextweek += datetime.timedelta(days=1)
        # 区间在一周内
        if day_nextweek > self.end_date:
            return 1
        weeks = ((self.end_date - day_nextweek).days + 1)/7
        weeks = int(weeks)
        if ((self.end_date - day_nextweek).days + 1)%7:
            weeks += 1
        if self.start_date < day_nextweek:
            weeks += 1
        return weeks

if __name__=='__main__':
    print str_to_date('')
    print str_to_date(None)
    print str_to_date_s('2016-10-23')


