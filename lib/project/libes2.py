# -*- coding: utf-8 -*- 


import json,io,os,sys,MySQLdb
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import httplib2,urllib,pinyin
from datetime import datetime
from datetime import date
from datetime import timedelta

from utils import ustr,umysql,ulog
from conf import settings

import sys  
  

es = Elasticsearch(["10.10.112.108","10.10.112.222"], http_auth=('admin', 'admin_000000'),sniff_on_start=True,sniff_on_connection_fail=True,sniffer_timeout=200)


def update_to_es_org(dats):

    if dats is None: return

    actions = []
    for dat in dats:
        action = {
               "_index": "zi_orgs",
               "_type": "org",
               "_id": dat["org_id"],
               "_source": dat
               }
        actions.append(action)

    helpers.bulk(es, actions)
    del actions
    

def update_to_es_brand(dats):

    if dats is None: return

    actions = []
    for dat in dats:
        action = {
               "_index": "zi_brand",
               "_type": "prod",
               "_id": dat["prod_id"],
               "_source": dat
               }
        actions.append(action)

    helpers.bulk(es, actions)
    del actions


def update_multi_cats_to_es(dats):


    if dats is None: return

    actions = []
    for dat in dats:
        action = {
        '_op_type': 'update',
        '_index': 'zi_brand',
        '_type': 'prod',
        "_id": dat["prod_id"],
        'doc': {
                'brand_cat_ids': dat["brand_cat_ids"],
                'brand_group_list': dat["brand_group_list"],
                'brand_target_list': dat["brand_target_list"]
            }
        }
        actions.append(action)
    try:
        helpers.bulk(libes2.es, actions)
        del actions
    except Exception, e:
        ulog.log('update cls error,ERROR:'+str(e))
    else:
        pass
    finally:
        pass
    


def get_need_update_cts(startdate,enddate):

    strsql = '''
    select 
    a.int_reg_id,GROUP_CONCAT(distinct b.int_int_cls_id) as GROUP_CONCAT_CLS,GROUP_CONCAT(distinct b.brand_group_list) as brand_group_list,GROUP_CONCAT(distinct b.brand_target_list) as brand_target_list
    from 
    (
    select int_reg_id from t_brand where int_ts >=%s and int_ts <=%s
    ) a,
    t_brand b
    where a.int_reg_id = b.int_reg_id  
    group by a.int_reg_id
    having count(distinct b.int_int_cls_id) >1 ;#should update
    '''

    data = umysql.db_getrd(settings.CONN_MYSQL_BRAND_YUHAN_SRC,strsql,startdate,enddate)
    if data is None:
        print 'no cls need to update....'
    else:
        k = 0;
        ls = []
        for line in data:
            _t = {}
            _t["prod_id"] = str(line[0])
            _t["brand_cat_ids"] =line[1].split(',')
            _t["brand_group_list"] =line[2].split(',')
            _t["brand_target_list"] =line[3].split(',')

            ls.append(_t)

            if k%500==0:
                print 'update cls lines:'+str(k)
                update_cls_to_es(ls)
                #print ls
                del ls[:]
            k+=1

        if len(ls)>0:
            #print ls
            update_cls_to_es(ls)

        del ls

        print 'update cls finished...'





def getRdCount(startdate,enddate):

    data =umysql.db_getrd(settings.CONN_MYSQL_BRAND_YUHAN_SRC,"select count(0) from t_brand where int_ts >= %s and  int_ts <=%s",startdate,enddate)
    if data is None:
        return 0
    else:
        return data[0][0]





def get_brand_Data(ipage,startdate,enddate):

    page_size = 5000
    rlist = []
    conn=MySQLdb.connect(**settings.CONN_MYSQL_BRAND_YUHAN_SRC)
    strsql = '''select 
                a.int_reg_id,str_name,int_int_cls_id, int_pre_pub_id, int_reg_pub_id,date_app_at,date_pre_pub,date_reg_pub,date_exclusive_begin,date_exclusive_end ,
                date_sub_design,date_int_reg,date_priority,
                str_reg_name_cn,str_reg_name_eng,str_reg_addr_cn,str_reg_addr_eng,
                str_agent_name,str_color_claimed,
                e_type,bool_zh_zhuming,bool_zh_chiming,
                bool_jointly_owned,bool_invalid,
                int_office_id,int_area_id,
                str_process_list,str_target_list,str_group_list,
                str_remark,int_ts

                from t_brand  a
                where int_ts >= %s and  int_ts <=%s


                '''

    strsql += 'limit ' + str((ipage-1)*page_size)+','+str(page_size)
    #print strsql

    try:
        conn.set_character_set('utf8')
        cur = conn.cursor()
        cur.execute(strsql,(startdate,enddate))
        data =cur.fetchall()
        for a in data:

            _t = {}
            _t["prod_id"]=_t["reg_id"] = _t["reg_id_i13"] = str(a[0])
            _t["prod_name"]=a[1]
            _t["brand_cat_ids"] = [str(a[2])] #不考虑多个类的问题,以后再说;
            _t["pre_pub_id"] = str(a[3])
            _t["reg_pub_id"] = str(a[4])
            #reg_pub_id_i13
            _t["date_app_at"] = a[5]
            _t["date_pre_pub"] = a[6]
            _t["date_reg_pub"] = a[7]
            _t["date_exclusive_begin"] = a[8]
            _t["date_exclusive_end"] = a[9]

            _t["date_sub_design"] = a[10]
            _t["date_reg_i13"] = a[11]
            _t["date_priority"] = a[12]

            #'reg_org_id':'',

            _t['reg_org_type'] =getOrgType(a[13]) #0 as com

            #print json.dumps(a[13]).decode('unicode-escape')+":"+str(str(a[13]).find('公司'))+':'+str(getOrgType(a[13]))

            _t["reg_org_name_cn"] = a[13]
            _t["reg_org_name_en"] = a[14]
            _t["reg_org_addr_cn"] = a[15]
            _t["reg_org_addr_en"] = a[16]


            
            #'agent_id':'',
            _t["agent_name"] = a[17]
            #_t["agent_region_id"] = a[17]


            _t["imageid"] = _t["prod_id"]
            #'doc_pages':['102121.1'], 

            _t["color_claimed"] =a[18]

            _s = set()
            if a[19] is not None:
                _s.add(a[19].strip(u'商标'))
            _s.add('著名' if a[20]==1 else '')
            _s.add('驰名' if a[21]==1 else '')

            _t["brand_type"] =list(_s)




            _t["is_jointly_owned"] =a[22]
            _t["is_invalid"] =a[23]

            _t["reg_gov_office_id"] =a[24]
            _t["reg_gov_area_id"] =a[25]


            _t["process_list"] = []
            _t["status"] = [a[26]]
            _t["brand_target_list"] = a[27] if a[27] is None else  (a[27].split("；") if a[27].find("；")>=0 else a[27].split(";"))
            _t["brand_group_list"] = a[28] if a[28] is None else (a[28].split("；") if a[28].find("；")>=0 else a[28].split(";"))
            _t["remark"] = a[29]
            _t["timestamp"] = a[30]

            _t["skpyin"] = [ustr.get_pinyin(unicode(_t["prod_name"]))]
            _t["skeng"]=[]


            rlist.append(_t)

        #print json.dumps(rlist, indent=2,cls=CJsonEncoder).decode('unicode-escape')
        return rlist

    except Exception, e:
        print e
        ulog.log('t_brand error page:' + str(ipage)+',ERROR:'+str(e))
    finally:
        cur.close()
        conn.close()



def getOrgType(name):  #判断公司还是个人;

    if name is None:
        return 0
    if name.find('公司')>=0 or name.find('厂')>=0 or name.find('有限')>=0 or name.find('group')>=0 or name.find('社')>=0 or name.find('Ltd')>=0 or name.find('集团')>=0 or name.find('协会')>=0 or name.find('所')>=0:
        if len(name)/3>3: return 0
        else: return 1
    else:
        if len(name)/3>15: return 0
        else:return 1


def get_pinyin(str1):

    if str1=='':return ''
    
    list1 =tuple(str1)

    bl_lst = True
    bl_this = True

    str1 = ''
    str2 = ''

    for a in list1:

        bl_this = ustr.is_chinese(a)

        if bl_lst==bl_this:
            str1+=a
        else:
            if not bl_this:
                str1 = pinyin.get(str1,' ')

            str2+=str1+' '
            str1=a
        
        bl_lst = bl_this

    if bl_this:
        str1 = pinyin.get(str1,' ')

    str2+=str1

    del list1

    return str2.strip()


