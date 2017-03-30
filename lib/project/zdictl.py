        # -*-coding:utf-8-*- #
from utils import udate,umysql
from conf import settings

def GetLocalTime():
    return udate.date_to_str(datetime.datetime.now())

def GetYesterday():
    return udate.date_to_str(datetime.datetime.now()+ datetime.timedelta(days=-1))


def getlastJobRuntime(job_id):
    strsql = "select LastExecuteTime from R_DATASOURCE_JOB where JobId = %s"

    data = umysql.db_getrd(settings.CONN_MYSQL_PAST_ZI_BI,strsql,(job_id))

    if data is None:
        return '1900-01-01 00:00:00'
    else:
        return udate.str_to_date(data[0][0])



def updateLastJobRuntime(lastExecTime,lastDsTime,lastid,job_id):
    strsql = "update R_DATASOURCE_JOB set LastExecuteTime = %s,LastExecuteDsUpdateTime = %s,LastExecuteDsKeyId=%s  where JobId = %s"

    k = umysql.dbExecute(settings.CONN_MYSQL_PAST_ZI_BI,strsql,lastExecTime,lastDsTime,lastid,job_id)
    if k==-1:
        ulog.log('comon updateLastJobRuntime Failed ...')
    else:
        ulog.log('comon updateLastJobRuntime,Success...')
