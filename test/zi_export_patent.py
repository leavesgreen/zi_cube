# -*- coding: utf-8 -*- 


import multiprocessing 

import time,csv,hashlib
import libes2
import json,io,os,sys,MySQLdb
from elasticsearch import Elasticsearch
import httplib2,urllib
from pymongo import MongoClient



def GetData(queue):

    lastid ='0'
    page_size=1000;
    icount = 0
    while True:
        print 'start handling lastid....'+str(lastid)
        
        lastid_new = lastid

        conn=MySQLdb.connect(host='10.10.107.4',user='root',passwd='000000',port=3306,db="zi")

        if queue.full():
            time.sleep(3)
            continue


        strsql = 'select * from T_PROD where prod_type = 1 and prod_id  > %s limit 0, %s'
        conn.set_character_set('utf8')
        cur = conn.cursor()
        try:
            cur.execute(strsql,(lastid,page_size))
            data =cur.fetchall()
            if data:
                lastid_new = data[-1][0]
                icount = icount+len(data)
                queue.put(data)
                print str(os.getpid()) + '(put):' + str(time.time())+".lastid:"+str(lastid)+",rows:"+str(icount)

        except Exception, e:
            print e
            libes2.writeLog('T_PROD error lastid:' + str(lastid)+',ERROR:'+str(e))
        finally:
            cur.close()
            conn.close()

        if not lastid_new == lastid:
            lastid = lastid_new
        elif icount>13000000:
            libes2.writeLog('T_PROD finished lastid:' + str(lastid))


def get_inner_str(t):
    
    if t is None or str(t)=="" or len(str(t))==0:
        return "0"
    elif type(t)== list:
        return ",".join(t)
    else: 
        return str(t)

def get_str(a):
    if a is None:return ''
    else: return str(a).replace('\r','').replace('\n','<br/>')

# output worker
def outputQ(queue,lock):
    


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
            lastid = a[0]

            line = list(a)
            
            if True:
                line[21]=get_str(line[21])

                line.append(line[21]) #region_temp_str

                line[5] = get_str(line[5])

                line[17] = get_str(line[17])
                line[16]=str(hashlib.md5(line[17]).hexdigest())+str(len(line[17]))

                line[19]= get_str(line[19])
                
                if(line[19].find('|')>0):
                    line.append(line[19].split('|')[0]) #temp postcode
                    line[19]=line[19].split('|')[1]
                else:
                    line.append('')

                line[21]=''
                line[48]=get_str(line[48])#48.remark
                line[49]=get_str(line[49])

            lines.append(line)
        
        write_to_csv(lines)

        print 'write to csv finished ,lastid:'+str(lastid)


def write_to_csv(lines):
    writer = csv.writer(open('./all_patents.csv',"ab"),quoting=csv.QUOTE_ALL)
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
