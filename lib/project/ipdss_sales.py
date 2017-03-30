
# -*- coding: utf-8 -*-

import sys

import  json,MySQLdb,io,uuid
import traceback,StringIO,urllib2,cStringIO

from datetime import datetime,timedelta
import calendar as calendar

from utils import ulog,udate,umysql,ustr,utils
from utils.cache import miniCache as mcache

CONN_MYSQL_PAST_ZI_BI = {'host':'10.10.113.1','user':'root','passwd':'111111', 'port':3306, 'db':"bi"}


def GetMainData(user,**kwgs):

    #getcache,cache refresh??

    DEPT_USER_ACCESS_DIC = get_fromcache('DEPT_USER_ACCESS_DIC')

    user = str(user)
    
    end_date = datetime.now()


    finishrate = 1

    if kwgs.has_key('enddate'):
        end_date = udate.str_to_date_s(kwgs.get("enddate",None))

    if kwgs.has_key('finishrate'):
        finishrate =ustr.atof(kwgs.get("finishrate"))/100.0

    if finishrate==0:finishrate=1
    
    print end_date


    
    strsql= ''

    ilevel = find_user_key(DEPT_USER_ACCESS_DIC,user)

    if not ilevel==0: #管理员不让看业务员的,太多;
        strsql = get_order_sql(4)

   

    if ilevel <=3:
        strsql += " union " +get_order_sql(3,True if ilevel==0 else False)
    if ilevel <=2:
        strsql += " union " +get_order_sql(2,True if ilevel==0 else False)
    if ilevel <=1:
        strsql += " union " +get_order_sql(1,True if ilevel==0 else False)

    strsql = strsql.strip().strip('union')

    print ilevel

    #防注入
    strwhere = "  and a.STATUS <>-1  and year(datetimeFirstRceipt)='"+str(udate.year(end_date))+"' and month(datetimeFirstRceipt) = '"+str(udate.month(end_date))+"' and day(datetimeFirstRceipt) <='"+str(udate.day(end_date))+"'"
    group_sql = strsql.format(group_by_day='', group_select_day=  " 0 as iday," ,id_emp=user,sql_where=strwhere,budget_day=str(udate.day(end_date)))

    strwhere = " and a.STATUS <>-1  and year(datetimeFirstRceipt)='"+str(udate.year(end_date))+"' and month(datetimeFirstRceipt) = '"+str(udate.month(end_date))+"' and day(datetimeFirstRceipt) ='"+str(udate.day(end_date))+"'"
    
    mxsql = strsql.format(group_by_day=',day(datetimeFirstRceipt)', group_select_day= 'day(datetimeFirstRceipt) as iday,' ,id_emp=user,sql_where=strwhere,budget_day=str(udate.day(end_date)))

    
    

    #print mxsql
    #print group_sql

    rlist = get_order_data(mxsql,group_sql,finishrate)


    #如果是ilevel=0,处理总经办为父节点
    if ilevel==0:
        for i in range(0,len(rlist)):
            if (rlist[i]["key_fid"] == "0" or rlist[i]["key_fid"] == "AREA_19") and rlist[i]["key_id"]<>"AREA_19":
                rlist[i]["key_fid"] ="ALL19"

            if rlist[i]["key_id"]=="AREA_19":
                rlist[i]["key_id"] ="ALL19"


    return rlist



def getworkdays(str_enddate):

    dd1 = udate.str_to_date_s(str_enddate)
    if udate.year(dd1)==1900:
        dd1 = datetime.now()
        str_enddate = udate.date_to_str_s(dd1)


    _t = calendar.monthrange(udate.year(dd1),udate.month(dd1))

    
    d1str= udate.date_to_str(dd1,'%Y-%m-')+'01'
    d2str=udate.date_to_str(dd1,'%Y-%m-')+str(_t[1])
    
    workdic={}
    a1 = udate.workDays(udate.str_to_date_s(d1str),udate.str_to_date_s(d2str))
    a2 = udate.workDays(udate.str_to_date_s(d1str),dd1)

    workdic["alldays"] = a1.daysCount()
    workdic["pastdays"] = a2.daysCount()
    workdic["leftdays"] =workdic["alldays"] - workdic["pastdays"] 
    workdic["finishrate"] =  round(100*float(workdic["pastdays"]) /workdic["alldays"],2)

    return workdic


def get_order_data(mxsql,group_sql,finishrate):


    USER_DIC = get_fromcache('USER_DIC')
    DEPT_DIC = get_fromcache('DEPT_DIC')
    PER_COUNT_DIC = get_fromcache('PER_COUNT_DIC')
    DEPT_MANAGER_DIC = get_fromcache('DEPT_MANAGER_DIC')
    
    tmpdic = {}
    #
    #print mxsql
    data = umysql.db_getrd(CONN_MYSQL_PAST_ZI_BI,mxsql)
    if not data is None:
        for d in data:
            tmpdic[d[3]] = 0 if d[6] is None else d[6]

    


    group_data = umysql.db_getrd(CONN_MYSQL_PAST_ZI_BI,group_sql)

    rlist=[]

    if not group_data is None:

        for d in group_data:

            t={}
            t['key_id'] =d[3]

            dep_key =  t['key_id'].split('_')[1] if t['key_id'].find('_')>0 else ''

            t['key_fid'] =d[4]
            t['key_name'] =d[5]

            t['main_per'] = '' if DEPT_MANAGER_DIC is None else USER_DIC.get(DEPT_MANAGER_DIC.get(t['key_id'],''))

            t['budget_mon'] = 0.0 if d[7] is None else float( d[7])
  
            t['budget_day'] = 0.0 if d[8] is None else float( d[8])
            t['actual_day'] = float(tmpdic.get(t['key_id'],0))

            t['actual_mon_accum'] = 0.0 if d[6] is None else float(d[6])

            t['rate_got'] = 0.0 if  t['budget_mon']==0 else round(100*float(t['actual_mon_accum'])/t['budget_mon'],2)
            t['rate_color_got'] = round(t['rate_got']/finishrate,2)

            t['per_count'] = 0 if PER_COUNT_DIC is None else PER_COUNT_DIC.get(dep_key,1)

            t['avg_per_actual_mon'] = 0.0 if  t['per_count']==0 else round(float(t['actual_mon_accum'])/t['per_count'],2)

            rlist.append(t)


    return rlist

def get_order_sql(ilevel,ismanager=False):

    str_access = '''
        AND 
        (
        a.ZIDeptAreaTemp in(select AccessCode from ZI_BASE_ACCESS where  IdEmp= '{id_emp}' and ResType = 'AREA' )
        or
        a.ZIDept in(select AccessCode from ZI_BASE_ACCESS where  IdEmp= '{id_emp}' and ResType = 'DEPT' )
        or
        a.ZIDeptGroupTemp in(select AccessCode from ZI_BASE_ACCESS where  IdEmp= '{id_emp}' and ResType = 'GROUP' )
        or
        a.ZIPerSaler in(select AccessCode from ZI_BASE_ACCESS where  IdEmp= '{id_emp}' and ResType = 'EMP' )
        )
    '''

    strsql_area = '''
        select year(datetimeFirstRceipt) as iyear,  
        month(datetimeFirstRceipt) as imon,
        {group_select_day}
        concat('AREA_',ZIDeptAreaTemp) as key_id,
        '0' as key_fid,
        b.DeptName as key_name,
        sum(a.NAmtOrder) as actual_day,
        c.BudgetAmt as budget_mon,
        c2.BudgetAmt as buget_day
        from ZI_BZ_ORDER a
        left join ZI_COMMON_DEPTS b on a.ZIDeptAreaTemp = b.IdDept
        left join ZI_BZ_BUDGET c on c.iyear = year(datetimeFirstRceipt) and c.imon = month(datetimeFirstRceipt) and c.iday = '0' and c.ResType = 'AREA' and c.ResCode = a.ZIDeptAreaTemp
        left join ZI_BZ_BUDGET c2 on c2.iyear = year(datetimeFirstRceipt) and c2.imon = month(datetimeFirstRceipt) and c2.iday = {budget_day} and c2.ResType = 'AREA' and
c2.ResCode = a.ZIDeptAreaTemp
        where 1=1 '''
    if not ismanager: strsql_area+= str_access

    strsql_area+=' {sql_where}  group by year(datetimeFirstRceipt) ,month(datetimeFirstRceipt){group_by_day}, ZIDeptAreaTemp'

    strsql_dept ='''
        select year(datetimeFirstRceipt) as iyear,  
        month(datetimeFirstRceipt) as imon,
        {group_select_day}
        concat('DEPT_',ZIDept) as key_id,
        concat('AREA_',ZIDeptAreaTemp) as key_fid,
        b.DeptName as key_name,
        sum(a.NAmtOrder) as actual_day,
        c.BudgetAmt as budget_mon,
        c2.BudgetAmt as buget_day
        from ZI_BZ_ORDER a
        left join ZI_COMMON_DEPTS b on a.ZIDept = b.IdDept
        left join ZI_BZ_BUDGET c on c.iyear = year(datetimeFirstRceipt) and c.imon = month(datetimeFirstRceipt) and c.iday = '0' and c.ResType = 'DEPT' and c.ResCode = a.ZIDept
        left join ZI_BZ_BUDGET c2 on c2.iyear = year(datetimeFirstRceipt) and c2.imon = month(datetimeFirstRceipt) and c2.iday = {budget_day}  and c2.ResType = 'DEPT' and
c2.ResCode = a.ZIDept
        where 1=1 '''
    if not ismanager: strsql_dept+= str_access
    strsql_dept+=' {sql_where} group by year(datetimeFirstRceipt) ,month(datetimeFirstRceipt){group_by_day}, ZIDept,ZIDeptAreaTemp'

    strsql_group='''
        select year(datetimeFirstRceipt) as iyear,  
        month(datetimeFirstRceipt) as imon,
        {group_select_day}
        concat('GROUP_',ZIDeptGroupTemp) as key_id,
        concat('DEPT_',ZIDept) as key_fid,
        b.DeptName as key_name,
        sum(a.NAmtOrder) as actual_day,
        c.BudgetAmt as budget_mon,
        c2.BudgetAmt as buget_day
        from ZI_BZ_ORDER a
        left join ZI_COMMON_DEPTS b on a.ZIDeptGroupTemp = b.IdDept
        left join ZI_BZ_BUDGET c on c.iyear = year(datetimeFirstRceipt) and c.imon = month(datetimeFirstRceipt) and c.iday = '0' and c.ResType = 'GROUP' and c.ResCode = a.ZIDeptGroupTemp
        left join ZI_BZ_BUDGET c2 on c2.iyear = year(datetimeFirstRceipt) and c2.imon = month(datetimeFirstRceipt) and c2.iday = {budget_day}  and c2.ResType = 'GROUP' and
c2.ResCode = a.ZIDeptGroupTemp
        where 1=1 '''
    if not ismanager:  strsql_group+= str_access

    strsql_group+=' {sql_where}  group by year(datetimeFirstRceipt) ,month(datetimeFirstRceipt){group_by_day}, ZIDept,ZIDeptAreaTemp,ZIDeptGroupTemp  '

    strsql_emp = '''
        select year(datetimeFirstRceipt) as iyear,  
        month(datetimeFirstRceipt) as imon,
        {group_select_day}
        concat('EMP_',ZIPerSaler) as key_id,
        concat('GROUP_',ZIDeptGroupTemp) as key_fid,
        b.per_name as key_name,
        sum(a.NAmtOrder) as actual_day,
        c.BudgetAmt as budget_mon,
        c2.BudgetAmt as buget_day

        from ZI_BZ_ORDER a
        left join ZI_COMMON_EMPLOYEES b on a.ZIPerSaler = b.IdEmp
        left join ZI_BZ_BUDGET c on c.iyear = year(datetimeFirstRceipt) and c.imon = month(datetimeFirstRceipt) and c.iday = '0' and c.ResType = 'EMP' and c.ResCode = a.ZIPerSaler
        left join ZI_BZ_BUDGET c2 on c2.iyear = year(datetimeFirstRceipt) and c2.imon = month(datetimeFirstRceipt) and c2.iday = {budget_day}  and c2.ResType = 'EMP' and
c2.ResCode = a.ZIPerSaler
        where 1=1 '''

    if not ismanager: strsql_emp+= str_access
    strsql_emp+=' {sql_where} group by year(datetimeFirstRceipt) ,month(datetimeFirstRceipt){group_by_day}, a.ZIDept,ZIDeptAreaTemp,ZIDeptGroupTemp,ZIPerSaler'

    if ilevel ==1:
        return strsql_area
    elif ilevel ==2:
        return strsql_dept
    elif ilevel==3:
        return strsql_group
    elif ilevel==4:
        return strsql_emp
    else:
        return ''


def get_deptList(user):
    rlist = []

    #ilevel=0,才写入none值的查询;其实不用写;其时已经去掉了过滤条件;

    if user is None or user =='':
        return rlist

    DEPT_USER_ACCESS_DIC = get_fromcache('DEPT_USER_ACCESS_DIC')
    ilevel = find_user_key(DEPT_USER_ACCESS_DIC,user)

    strAccess = "$";

    if ilevel>0: #非管理员
        tmpsql = "select GROUP_CONCAT(AccessCode) from ZI_BASE_ACCESS as str1 where RefResType = 'BZ_ORDER' and ResType<> 'ALL' and ResType<> 'EMP' and IdEmp='"+user+"'"
        data = umysql.db_getrd(CONN_MYSQL_PAST_ZI_BI,tmpsql)
        if data is not None:
            strAccess+=','+data[0][0]





    strsql='''
    select '{empid}' as IdEmp, 
    Case ilevel when 1 then 'AREA' when 2 then 'DEPT' when 3 then 'GROUP' end as   ResType, 
    d.idDept as AccessCode,d.DeptName as AccesName,
    concat((Case (ilevel-1) when 0 then '' when 1 then 'AREA' when 2 then 'DEPT' when 3 then 'GROUP' end),'_', d.FidDept) as PrtCode  
    from 
    ZI_COMMON_DEPTS d
    where 1=1
    and d.STATUS=0 and isBusiness=1 #if the manger, that's enough
    and ilevel in (1,2,3)
    '''
    if ilevel>0:
        strsql+=" and FIND_IN_SET(idDept,queryChildrenDept(queryChildrenDept('"+strAccess+"')))"


        strsql+='''
        union
        select
        a.IdEmp,a.ResType,a.AccessCode,b.per_name as AccesName,
        concat((Case ilevel when 0 then '' when 1 then 'AREA' when 2 then 'DEPT' when 3 then 'GROUP' end),'_', b.ZIDept) as PrtCode 
        from ZI_BASE_ACCESS a ,ZI_COMMON_EMPLOYEES b ,ZI_COMMON_DEPTS c
        where  a.IdEmp = '{empid}' and a.AccessCode = b.idemp and a.ResType='EMP' and RefResType = 'BZ_ORDER' and c.IdDept = b.ZIDept
        '''

    strsql = strsql.format(empid=user)
    data = umysql.db_getrd(CONN_MYSQL_PAST_ZI_BI,strsql)




    if not data is None:
        for d in data:
            #_name = get_forcombo_deptname(d[4],d[3])
            _name = get_forcombo_deptname(d[1],d[3])

            rlist.append({'id':d[1]+'_'+d[2],'fid':d[4],'name':_name})
    
    rlist = utils.get_PrtChd_list(rlist,'fid','id');

    rlist.insert(0,{'id':"",'fid':"-1","name":"<b>ALL</b>"}) #add the total node

    return rlist


def get_forcombo_deptname(PrtCode,name):

    '''
    if PrtCode.find('_')<0:
        return name
    else:
        restype = PrtCode.split('_')[0]
    '''
    restype = PrtCode #now use the absoluate level.

    if restype=='AREA':
        return ''.ljust(1,' ')+'<b>'+name+'</b>'
    elif restype=='DEPT':
        return ''.ljust(3,' ')+name
    elif restype=='GROUP':
        return ''.ljust(5,' ')+name
    elif restype=='EMP':
        return ''.ljust(7,' ')+name
    return name



def get_fromcache(cachekey):

    #未采用periodicCallback,不费那劲了
    tmp = mcache.getinstance().get(cachekey)
    if tmp is None:
        refreshCache()
        tmp = mcache.getinstance().get(cachekey)

    return tmp




def refreshCache():

    USER_DIC = {}
    DEPT_DIC ={}
    PER_COUNT_DIC={}
    DEPT_MANAGER_DIC = {}
    DEPT_USER_ACCESS_DIC = {}
    DEPT_LIST=[]
    

    strsql = "select idemp,per_name, ZIDept, a.status,b.isBusiness from ZI_COMMON_EMPLOYEES a left join ZI_COMMON_DEPTS b on a.ZIDept = b.IdDept "
    data = umysql.db_getrd(CONN_MYSQL_PAST_ZI_BI,strsql)
    
    if not data is None:
        for d in data:
            USER_DIC[d[0]]=d[1]

            #if d[3]<> -1 and d[4]==1:


    _now = datetime.now()
    #这个dict目前按月,当前月出,如果改为按日,需要修改这里的位置,同时查询方法也不能如此处理;
    strsql = "select ZIDept,perCount from ZI_COMMON_DEPT_PERCOUNT where iyear='"+str(udate.year(_now))+"' and imon='"+str(udate.month(_now))+"' and iday='0' and status=0 "
    #print strsql
    data = umysql.db_getrd(CONN_MYSQL_PAST_ZI_BI,strsql)
    if not data is None:
        for d in data:
            PER_COUNT_DIC[d[0]] = d[1]


    DEPT_LIST = []

    strsql = "select IdDept,FidDept,deptname,ilevel,isBusiness from ZI_COMMON_DEPTS where status <> -1" 
    data = umysql.db_getrd(CONN_MYSQL_PAST_ZI_BI,strsql)
    if not data is None:
        for d in data:
            DEPT_DIC[d[0]]=d[2]
            DEPT_LIST.append((d[0],d[1],d[3],d[2],d[4])) #iddept,fidept,ilevel,name,isbusiness.



    #递归人数；3->2
    ilevel=4
    while ilevel >=1:
        for d in DEPT_LIST:
            if d[2] ==ilevel:
                if PER_COUNT_DIC.has_key(d[0]):
                    if PER_COUNT_DIC.has_key(d[1]):
                        PER_COUNT_DIC[d[1]]+=PER_COUNT_DIC[d[0]]
                    else:
                        PER_COUNT_DIC[d[1]]=PER_COUNT_DIC[d[0]]
        ilevel-=1



    strsql = "select restype,AccessCode,idemp,isMain from ZI_BASE_ACCESS where ResType <> 'EMP';"
    data = umysql.db_getrd(CONN_MYSQL_PAST_ZI_BI,strsql)

    if not data is None:
        for d in data:
            DEPT_USER_ACCESS_DIC[d[0]+'_'+d[1]+'_'+d[2]] = d[2]
            if d[3]==1:
                DEPT_MANAGER_DIC[d[0]+'_'+d[1]]=d[2]

    mcache.getinstance().set('USER_DIC',USER_DIC,datetime.now()+timedelta(seconds=900))
    mcache.getinstance().set('DEPT_DIC',DEPT_DIC,datetime.now()+timedelta(seconds=900))
    mcache.getinstance().set('DEPT_MANAGER_DIC',DEPT_MANAGER_DIC,datetime.now()+timedelta(seconds=900))
    mcache.getinstance().set('PER_COUNT_DIC',PER_COUNT_DIC,datetime.now()+timedelta(seconds=900))
    mcache.getinstance().set('DEPT_USER_ACCESS_DIC',DEPT_USER_ACCESS_DIC,datetime.now()+timedelta(seconds=900))
    mcache.getinstance().set('DEPT_LIST',DEPT_LIST,datetime.now()+timedelta(seconds=900))

def find_user_key(dic,user):

    if dic is None :return 4
    #print len(dic)


    ilevel = 4

    for k in dic.keys():


        
        if str(dic[k])==user:
            print k
            #print dic[k]

            if k.find('ALL')>-1:
                ilevel=0
            elif k.find('AREA')>-1 and ilevel >1:
                ilevel = 1
            elif k.find('DEPT')>-1 and ilevel >2 :
                ilevel = 2
            elif k.find('GROUP')>-1 and ilevel >3:
                ilevel = 3

    return ilevel