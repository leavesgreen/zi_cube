#!/usr/bin/env python
# -*-coding:utf-8-*- #


import time,datetime,uuid
import os,MySQLdb
import sys



reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append('./lib')
import utils.utils

tmp_connstr = {'host':'10.10.107.4','user':'root','passwd':'000000', 'port':3306, 'db':"zi"}


def GetLocalTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

def GetYesterday():
    return (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")


def getlastJobRuntime(job_id):
    strsql = "select LastExecuteTime from R_DATASOURCE_JOB where JobId = %s"
    data = dbGetRd(tmp_connstr,strsql,(job_id))
    if data is None:
        return '1900-01-01 00:00:00'
    else:
        try:
            return datetime.datetime.strftime(data[0][0],"%Y-%m-%d %H:%M:%S")
        except Exception,e:
            return '1900-01-01 00:00:00'


def getNextJobRuntime(job_id):
    return  datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:00")


def updateLastJobRuntime(lastExecTime,lastDsTime,lastid,job_id):
    strsql = "update R_DATASOURCE_JOB set LastExecuteTime = %s,LastExecuteDsUpdateTime = %s,LastExecuteDsKeyId=%s  where JobId = %s"

    k = dbExecute(tmp_connstr,strsql,lastExecTime,lastDsTime,lastid,job_id)
    if k== -1:
        writeLog('comon updateLastJobRuntime Failed ...')
    else:
        writeLog('comon updateLastJobRuntime,Success...')




def dbGetRd(connstr,strsql,*args):

    conn=MySQLdb.connect(**connstr)
    try:
        conn.set_character_set('utf8')
        cur = conn.cursor()
        cur.execute(strsql,args)
        data =cur.fetchall()
        return data
    except Exception, e:
        print e
        writeLog('comon DBGetRd,ERROR:'+str(e))
    finally:
        cur.close()
        conn.close()

def dbExecute(connstr,strsql,*args):
    try:
        conn = MySQLdb.connect(**connstr)
        conn.set_character_set('utf8')
        cur = conn.cursor()
        print strsql
        k = cur.execute(strsql,args)
        conn.commit()
        return k
    except Exception, e:
        print e
        writeLog('trademark_to_zkb:'+str("sql:" + strsql + ",ERROR:" + str(e)))
        return -1
    finally:
        cur.close()
        conn.close()
        

def KettleInsertToDb():
    #Today=(datetime.datetime.now() + datetime.timedelta(days=-2)).strftime("%Y-%m-%d %H:%M:%S")

    JOB_ID = "05.CRM3_TO_ZI_NEW"

    lastTime = getlastJobRuntime(JOB_ID)
    nextTime = getNextJobRuntime(JOB_ID)
    batchId = str(uuid.uuid1())

    print lastTime
    print nextTime


    kettle_path = '/home/dev/soft/kettle_5.0.1/data-integration/kitchen.sh'

    #kettle_path = 'F:/mysoft/bigdata/pentaho.soft/kettle_5.0.1/data-integration/Kitchen.bat'
    cmd_path = kettle_path + ' -rep=krepo_zi -user=admin -pass=admin -dir=/05.crm3_to_zi_new -level=Debug -job=crm_to_zi_new "' +lastTime+'" "' +  nextTime+'"  "'+batchId+'"'

    print cmd_path
    k = os.system(cmd_path)
    #k=0

    
    #RUN SQL
    #删除预算表中,受影响的自动计算得到的预算信息;
    if k==0:
        updateLastJobRuntime(nextTime,None,None,JOB_ID)
        writeLog("crm3_to_zkb.job.finished....Success"+str(datetime.datetime.now()))
    else:
        writeLog("crm3_to_zkb.job.finished....With error"+str(datetime.datetime.now()))


def writeLog(str):
    with open('./logs.txt','ab') as f:
        f.write("LOG:"+datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")+","+str+"\r\n")

if __name__ == '__main__':
    KettleInsertToDb()

    
