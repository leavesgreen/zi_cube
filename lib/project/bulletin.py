# -*- coding: utf-8 -*- 

import os.path

import pinyin,json,random,csv
from datetime import datetime
from datetime import date
from datetime import timedelta
import random

import MySQLdb
import utils

bulletinConn={'host':'10.10.100.31','user':'brandreader','passwd':'4t9scAG7','port':3306,'db':"bulletin"}
ziConn= {'host':'10.10.107.4','user':'root','passwd':'000000','port':3306,'db':"zi"}


def mssqlGet(msconn,strsql,*params):
    conn = pymssql.connect(**msconn)
    cur = conn.cursor()
    if not cur:
        raise(NameError,"连接数据库失败")

    cur.execute(strsql,params)
    resList = cur.fetchall()
    conn.close()
    return resList


#临时使用,用来生成分条款的商标数据,无实际意义;
def getBrandTerms(strName):
    conn=MySQLdb.connect(**ziConn)
    conn.set_character_set('utf8')

    list1 = []
    strsql = "select termCode,termFCode,termTitle,termType,ilevel from BrandTerms  where inUse=1 "
    try:
        
        cur = conn.cursor()
        cur.execute(strsql)
        data =cur.fetchall()
        for a in data:
            _t = {}
            _t["id"]=utils.atoi(a[0].replace('.',''))
            _t["pId"]=0 if a[1] is None else utils.atoi(a[1].replace('.',''))
            _t["name"] =a[0]+a[2].replace('\r',",").replace('\n',",")+"......"+str(random.uniform(0, 100) )+"|<span style='min-width:100px; background-color:green'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span>"
            _t["chkDisabled"]="true"
            list1.append(_t)

        return list1

    except Exception, e:
        print e
        utils.log('bulletin getBulletin,ERROR:'+str(e))
    finally:
        cur.close()
        conn.close()



def getProcesslits(regid):
    rlist = []
    conn=MySQLdb.connect(**bulletinConn)

    conn.set_character_set('utf8')

    strsql = "select str_type,date_at from t_progress where str_reg_id = '%s' order by date_at desc;" % regid

    
    try:
        
        cur = conn.cursor()
        cur.execute(strsql)
        data =cur.fetchall()
        for a in data:
            rlist.append(a)

        #print json.dumps(rlist).decode('unicode-escape')
        return rlist

    except Exception, e:
        print e
        utils.log('bulletin getProcesslits,ERROR:'+str(e))
    finally:
        cur.close()
        conn.close()

    return rlist

def getLastModifiedDate():

    lastdate = None
    conn=MySQLdb.connect(**bulletinConn)

    conn.set_character_set('utf8')

    strsql = "select str_value from t_config "

    

    try:
        
        cur = conn.cursor()
        cur.execute(strsql)
        data =cur.fetchone()
        if data is not None:
            lastdate = data[0] #datetime.strftime(data[0],'%Y-%m-%d')
        
        return lastdate
        

    except Exception, e:
        print e
        utils.log('bulletin getLastModifiedDate,ERROR:'+str(e))
    finally:
        cur.close()
        conn.close()

    return lastdate


def getBulletin(regid):
    rlist = []
    conn=MySQLdb.connect(**bulletinConn)

    conn.set_character_set('utf8')

    #strsql = "select str_reg_id,int_volumn,int_page from t_bulletin_content where str_reg_id ='%s' ;" % regid
    strsql = "select str_reg_id,int_volumn,int_page from t_bulletin_content where str_reg_id =%s ;"
    try:
        
        cur = conn.cursor()
        cur.execute(strsql,(regid))
        data =cur.fetchall()
        for a in data:
            rlist.append(a)

        #print json.dumps(rlist, indent=2).decode('unicode-escape')
        return rlist

    except Exception, e:
        print e
        utils.log('bulletin getBulletin,ERROR:'+str(e))
    finally:
        cur.close()
        conn.close()

#这个文件很大,需要异步和分拆服务来做;
def getBulletinImg(ivolumn,ipage):
    
    conn=MySQLdb.connect(**bulletinConn)

    strsql = "select bin_image from t_bulletin_image  where int_volumn=%s and int_page=%s; "
    try:
        
        cur = conn.cursor()
        cur.execute(strsql,(ivolumn,ipage))
        data =cur.fetchone()
        if data is not None:
        #print type(data)
            return data[0]
        

    except Exception, e:
        print e
        utils.log('bulletin getBulletin,ERROR:'+str(e))
    finally:
        cur.close()
        conn.close()

#暂时不包含crm3的商标图片
def get_brand_img(regid):
    
    conn=MySQLdb.connect(host='10.10.100.31',user='brandreader',passwd='4t9scAG7',port=3306,db="trademark")

    strsql = "select bin_image from t_image  where str_reg_id=%s ; "
    try:
        
        cur = conn.cursor()
        cur.execute(strsql,(regid))

        data =cur.fetchone()
        if data is not None:
            return data[0]


    except Exception, e:
        print e
        utils.log('get brand image from db,ERROR:'+str(e))
    finally:
        cur.close()
        conn.close()

    #get from http,should user async, or will block the server.










if __name__=='__main__':
    #'3956344'
    #print getBulletinImg('1043','893')
    print getBulletin('3956344')
    
  