# -*- coding: utf-8 -*- 

import os.path

import pinyin,json,random,csv
from datetime import datetime
from datetime import date
from datetime import timedelta


import MySQLdb
import utils

bulletinConn={'host':'10.10.100.31','user':'brandreader','passwd':'4t9scAG7','port':3306,'db':"trademark"}

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

        #print json.dumps(rlist, indent=2).decode('unicode-escape')
        return rlist

    except Exception, e:
        print e
        utils.log('bulletin getProcesslits,ERROR:'+str(e))
    finally:
        cur.close()
        conn.close()

    return rlist






if __name__=='__main__':
    #'3956344'
    #print getBulletinImg('1043','893')
    print getBulletin('3956344')
    
  