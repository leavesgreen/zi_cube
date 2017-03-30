# -*- coding: utf-8 -*-
import MySQLdb
import ulog


def db_getrd(connstr,strsql,*args):

    conn=MySQLdb.connect(**connstr)
    try:
        conn.set_character_set('utf8')
        cur = conn.cursor()
        cur.execute(strsql,args)

        '''
        if len(args)>0:
            cur.execute(strsql,args)
        else:
            cur.execute(strsql)
        '''
        data =cur.fetchall()
        return data
    except Exception, e:
        print e
        ulog.log('dbGetRd ERROR:'+str("sql:" + strsql + ",ERROR:" + str(e)))
    finally:
        cur.close()
        conn.close()

def db_getrd_bydic(connstr,strsql,dic):
    strsql+= " where 1=1 "
    ls1=[]
    #客户端自行判断其合法性;
    for k in dic.keys():
        strsql+= ' and '+str(k)+"=%"
        ls1.append(dic[k])

    return db_getrd(connstr,strsql,ls1)





def db_execute(connstr,strsql,*args):
    try:
        conn = MySQLdb.connect(**connstr)
        conn.set_character_set('utf8')
        cur = conn.cursor()
        #print strsql
        k = cur.execute(strsql,args)
        '''
        if len(args)>0:
            k = cur.execute(strsql,args)
        else:
            k =cur.execute(strsql)
        '''
        
        conn.commit()
        return k
    except Exception, e:
        print e
        ulog.log('dbExecute ERROR:'+str("sql:" + strsql + ",ERROR:" + str(e)))
        return -1
    finally:
        cur.close()
        conn.close()
        