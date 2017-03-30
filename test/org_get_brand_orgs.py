# -*- coding: utf-8 -*- 


import multiprocessing 

import time,datetime
import libes2
import json,io,os,sys,MySQLdb,shutil
import xlrd,uuid,hashlib
import csv,codecs
import jieba
import redis 


reload(sys)
sys.setdefaultencoding('utf-8')

r1 = redis.Redis(host='10.10.107.5', port=6379, db=1) 

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self






def init_redis():

    print 'start anync redis'


    reader = UnicodeReader(open('./org_matched_new.csv'))
    i=0
    for line in reader:
        r1.hset(line[0],'p_org_id',line[0])
        r1.hset(line[0],'n_org_id',line[0])
        print str(i)
        i+=1

    print 'finished anync redis'



def write_to_csv(fpath,line):

    writer = csv.writer(open(fpath,"ab"),quoting=csv.QUOTE_ALL)
    try:
      writer.writerow(line)
    except Exception,e:
      print e
      libes2.writeLog('insert db error:,ERROR:'+str(e))
    finally:
      print 'write to csv success...'
      del line




def get_search_txt(str1):
    
    ls1 = get_txts(str1)

    if len(ls1)>0:
      return ' AND '.join(ls1)

    return ls1


def get_txts(str1):
    stopwords = {}.fromkeys([u'公司', u'有限',u'责任',u'厂',u'店',u'区',u'县',u'省',u'自治区',u'市',u'co',u'ltd',u'股份',u'有限公司',u'有限责任公司',u'股份有限',u'股份有限公司',u' ',u''])
    ls1=[]

    set1 = set(jieba.cut(str1,cut_all=True))
    
    for s in set1:
        if s not in stopwords:
            ls1.append(s)

    del set1

    return ls1

def txt_like(txt1,txt2,rate):

    if txt1 is None:txt1 = ""
    if txt2 is None:txt2 = ""

    if txt1==txt2:return 1.0

    ls1 = get_txts(txt1)
    ls2 = get_txts(txt2)

    _all = len(ls2)

    #print json.dumps(ls1).decode('unicode-escape')
    #print json.dumps(ls2).decode('unicode-escape')

    if _all==0 :
        if len(ls1)==0:
            return 1
        else:
            return 0

    tmp = [x for x in ls1 if x in ls2]

    return rate*len(tmp)/float(_all);



        
if __name__=='__main__':

    #init_redis()
    #sys.exit(0)


    reader = UnicodeReader(open('./lastestbrand.csv'))

    out_path = './brand_out/'

    rlist = []
    dic = {}
    i=0
    
    for line in reader:
        #print line

        i+=1

        if i==1:
          continue


        print 'handling. line:'+str(i)

        if line is None or len(line)<50:
            print 'this line is invalid.....'
            continue

        #print line

        org_id = line[51]
        org_name =line[46]

        print 'line:'+str(i)+'......org_id:'+org_id+',org_name:'+org_name

        #判断是否已经存在对应,redis,如果已经有了;
        if org_name is None or org_name.strip() =='':
            print 'the name is empty....skiped...'
            continue

        if str(line[17])=="1":
            print 'the org type  is person.....skiped...'
            continue



        org_name = org_name.strip()

        if r1.hget(org_id,'p_org_id'):
            
            print 'already in redis'

            _brand_cats = r1.hget(org_id,'brand_cats')
            _brands = r1.hget(org_id,'brands')
            _n_org_id = r1.hget(org_id,'n_org_id')

            _brand_cats = '' if _brand_cats is None else _brand_cats
            _brands = '' if _brands is None else _brands
            _n_org_id = '' if _n_org_id is None else _n_org_id

            #加入到redis.

            r1.hset(org_id,'brand_cats',_brand_cats+","+line[19])
            r1.hset(org_id,'brands',_brands+","+line[8]+"-"+line[26])

            row=[]
            row.append(org_id)
            row.append(org_name)
            row.append(_n_org_id)
            row.append('')

            row.append(line[19])
            row.append(line[8]+"-"+line[26])

            
            f0 = str(abs(hash(org_id))%10000)+'.csv'

            write_to_csv(out_path+'/org_brand_mapping_'+f0,row)

            continue
        rlist=[]

        try:
            rlist = libes2.get_from_es(get_search_txt(org_name))
        except Exception,e:
            #should connect again...
            print str(e)
            pass

        if rlist is None or len(rlist)==0:
            print 'find no matched org.....,will be continue'
            continue
        
        dic = {}

        k=0
        max_score = rlist[0]['_score']

        for s in rlist:

            dic[k] = txt_like(s["org_name_cn"],org_name,s['_score']/max_score)
            k+=1

        
        #取最大值,且大于65
        dic =  sorted(dic.iteritems(),key=lambda d:d[1],reverse=True)
        
        if dic is None or len(dic)==0:
            print 'find no matched org.....,will be continue'
            continue
        
        print dic

        rs = rlist[dic[0][0]]
        
        #print rs



        print 'find in db...,incsvname:'+org_name+',findcode:'+str(rs["org_id"])+",findname:"+str(rs["org_name_cn"])+",score:"+str(dic[0][1])

        #已经处理的应该在数据库中加标记,最后一块儿加
        if dic[0][1] >0.8:
            
            row=[]
            r1.hset(org_id,'p_org_id',org_id)
            r1.hset(org_id,'n_org_id',rs["org_id"])

            r1.hset(org_id,'brand_cats',line[19])
            r1.hset(org_id,'brands',line[8]+"-"+line[26])

            row.append(org_id)
            row.append(org_name)
            row.append(rs["org_id"][0])
            row.append(rs["org_name_cn"][0])

            row.append(line[19])
            row.append(line[8]+"-"+line[26])

            #加入到redis.
            f0 = str(abs(hash(org_id))%10000)+'.csv'

            write_to_csv(out_path+'/org_brand_mapping_'+f0,row)

