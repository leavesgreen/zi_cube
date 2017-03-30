# -*- coding: utf-8 -*- 


import multiprocessing 

import time,csv
import libes2
import json,io,os,sys,MySQLdb
from elasticsearch import Elasticsearch
import httplib2,urllib
import pymongo
from pymongo import MongoClient

client=MongoClient('mongodb://10.10.113.9:27017/')



def GetData(queue):

    lastid =0
    page_size=1000;
    while True:
        print 'start handling lastid....'+str(lastid)
        
        lastid_new = lastid

        conn=MySQLdb.connect(host='10.10.100.31',user='root',passwd='xmmiou8015',port=3306,db="trademark")

        if queue.full():
            time.sleep(3)
            continue


        strsql = 'select int_id,str_reg_id from t_image where int_id > %s limit 0, %s'
        conn.set_character_set('utf8')
        cur = conn.cursor()
        try:
            cur.execute(strsql,(lastid,page_size))
            data =cur.fetchall()
            if data:
                lastid_new = data[-1][0]
                
                queue.put(data)
                print str(os.getpid()) + '(put):' + str(time.time())+".lastid:"+str(lastid)

        except Exception, e:
            print e
            libes2.writeLog('t_image error lastid:' + str(lastid)+',ERROR:'+str(e))
        finally:
            cur.close()
            conn.close()

        if not lastid_new == lastid:
            lastid = lastid_new
        elif lastid==16283491:
            libes2.writeLog('t_image finished lastid:' + str(lastid))


def get_inner_str(t):
    
    if t is None or str(t)=="" or len(str(t))==0:
        return "0"
    elif type(t)== list:
        return ",".join(t)
    else: 
        return str(t)


# output worker
def outputQ(queue,lock):
    
    db=client.zi
    brand=db.brand

    while True:
        k=0
        if queue.empty():    
            if k >30:
                break
                libes2.writeLog('all finished')        
            time.sleep(3)
            k +=1
            continue
        lastid = 0

        rlist = queue.get()
        lines = []
        
        for a in rlist:
            _id = a[1]
            lastid = a[0]

            line = []
            _t = brand.find_one({"_id":_id},{'prod_name':1,'brand_cat_ids':1,'brand_group_list':1,'is_invalid':1})
            if _t:
                line.append(lastid)
                line.append(_id)
                line.append('03')
                line.append('100')
                line.append(get_inner_str(_t.get("brand_cat_ids")))
                line.append(get_inner_str(_t.get("brand_group_list")))
                line.append('1')
                line.append(_t.get("is_invalid"))
                line.append(0)
                line.append(_t.get("prod_name"))
                line.append(0)
                line.append(0)

            lines.append(line)
        
        write_to_csv(lines)

        print 'write to csv finished ,lastid:'+str(lastid)


def write_to_csv(lines):
    writer = csv.writer(open('d:/temp/protect_imgs.csv',"ab"),quoting=csv.QUOTE_ALL)
    try:
      writer.writerows(lines)
    except Exception,e:
      print e
      libes2.writeLog('write to file db error:,ERROR:'+str(e))
    finally:
      del lines
      


record1 = []   # store input processes
record2 = []   # store output processes
lock  = multiprocessing.Lock()    # To prevent messy print
queue = multiprocessing.Queue(20)

if __name__=='__main__':
    # input processes
    for i in range(1):
        process = multiprocessing.Process(target=GetData,args=(queue,))
        process.start()
        record1.append(process)

    # output processes
    for i in range(1):
        process = multiprocessing.Process(target=outputQ,args=(queue,lock))
        process.start()
        record2.append(process)


    for p in record1:
        p.join()

    

    for p in record2:
        p.join()
     
    for p in record2:
        print 'all finished...'
        #p.terminate()

    queue.close()  # No more object will come, close the queue