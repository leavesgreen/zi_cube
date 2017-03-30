# -*- coding: utf-8 -*- 


import multiprocessing 

import time,datetime
import libes2
import json,io,os,sys,MySQLdb,shutil
import xlrd,uuid,hashlib
import csv,codecs

reload(sys)
sys.setdefaultencoding('utf-8')

globalDic={}
globalExtelDic={}
globalPostDic={}
globalMoblieDic={}

def GetData(filepath):
    
    
    try:
      
      for fd in os.listdir(filepath):
          #handle file first.
          newpath = filepath+fd
          
          if os.path.isfile(newpath):
              try:
                  write_to_db(newpath)
                  #libes2.writeLastid(newpath)
              except Exception, e:
                  print e
                  libes2.writeLog('ERROR WHEN INSERT: CAUGHT FILE:'+newpath+",ERROR:"+str(e))
              
          else:
              GetData(newpath+"/")
              
          libes2.writeLog('update folder finished ' + newpath)
          
    except Exception, e:
        print e

        

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


def write_to_db(fullpath):
    print 'start handling path:'+fullpath
    
    reader = UnicodeReader(open(fullpath))
    
    #conn=MySQLdb.connect(host='localhost',user='root',passwd='000000',port=3306,db="zi")
    #conn.set_character_set('utf8')
    #cur = conn.cursor()
    try:
    

      i=1
      tmpdic = {}
      idcol = 1
      geocol = 0
      rlist = []
     
      for line in reader:
          
          #line.decode('gb3212').encode('utf-8')
          tlist=[]

          if i==1:
              
              #with open('./alltales_head_01.txt','ab') as f:
              #    f.write(','.join(line) +"\r\n")
              #break
              
              COL_N=0
              for th in line:
                  if COL_N==0:
                    th = th[1:]

                  if th==u'行政区号':
                    geocol = COL_N
                    
                  if globalDic.has_key(th):

                      DB_N =str(globalDic[th])

                      tmpdic[DB_N]=COL_N
                    
                      if DB_N=='1': 
                          idcol=COL_N

                  COL_N+=1
              print 'idcol:'+str(idcol)

              i+=1
              continue

          

          for DB_N in range(24): #the number of the db want.
              
              
              str1=None
              
              if  tmpdic.has_key(str(DB_N)):
                  COL_N = tmpdic[str(DB_N)]
                  str1 = line[COL_N].replace('\n','').replace('\r','<br/>')
                  
              if DB_N==0: 
                  tlist.append(str(hashlib.md5(line[idcol]).hexdigest())+str(len(line[idcol])))
              elif DB_N==22: 
                  tlist.append(fullpath) #remark
              elif DB_N==16:
                  tlist.append(getnumbers(str1))
              elif DB_N==20:
                  tlist.append(getdate_temp(str1))

              elif DB_N>16 and DB_N<20:
                  tlist.append(getlastnumbers(str1))
              else:
                  tlist.append(str1)

          #add region
          if geocol<>0:
            tlist.append(line[geocol])
            
          else:
            tlist.append(get_geo(tlist[5],tlist[12],tlist[8],tlist[6]))
            
              
              #print DB_N

          #print tlist
          
          

          try:
              '''
              strsql = 'insert into zi_common_org(org_id,org_name_cn,org_desc,uname_contact,uposition_contact,Extel,Tel,Fax,mobile,email,uname_holder,org_addr_cn,postcode,org_gov_bzscope,ZIIndustryDesc,org_gov_type,org_gov_bzmode,registered_capital,org_revenues,org_pers_count,date_foundation,region_temp_str,remark,website,geo_region_id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

              cur.execute(strsql,tlist)

              conn.commit()
              '''
              rlist.append(tlist)
              if i%10000==0:
                write_to_csv(rlist)
               

          except Exception, e:
              print e
              libes2.writeLog('insert db error:' + str(line[2])+',ERROR:'+str(e))
          finally:
             #print 'handled......rows:'+str(i)
              i+=1


      #the left
      if len(rlist)>0 :
          write_to_csv(rlist)
      


    except Exception, e:
        print e
    '''
    finally:
        cur.close()
        conn.close()
    '''        

def write_to_csv(lines):
    writer = csv.writer(open('./org_access_db.csv',"ab"),quoting=csv.QUOTE_ALL)
    try:
      writer.writerows(lines)
    except Exception,e:
      print e
      libes2.writeLog('insert db error:,ERROR:'+str(e))
    finally:
      print 'write to csv success...lines done:'+str(len(lines))
      del lines[:]
      

def get_geo(extel,postcode,mobile,tel):

    extel = '' if extel is None else extel.strip()
    postcode = '' if postcode is None else postcode.strip()
    mobile = '' if mobile is None else mobile.strip()
    tel='' if tel is None else tel.strip()

    rtn = ''

    if  extel <> '':
      rtn =globalExtelDic.get(extel)


    if (rtn is  None or rtn=='') and postcode<> '':
      rtn = globalPostDic.get(postcode)

    if (rtn is  None or rtn=='') and mobile <> '':
      rtn= globalMoblieDic.get(mobile[:7])

    if (rtn is  None or rtn=='') and tel <> '':
      rtn= globalMoblieDic.get(tel[:7])

    #print 'extel:'+extel+',postcode:'+postcode+',mobile:'+mobile+",geoid:"+rtn

    return rtn

def getnumbers(str1):
    #
    if str1 is None: return 0

    ns = ''
    for s in str1:
        if is_number(s) or s=='.':
          ns+=s
    return atof(ns)


def getlastnumbers(str1):
    if str1 is None:return 0
    ns =''
    tl = len(str1)
    bl = False
    for i in range(tl):
        s = str1[tl-i-1]
        if is_number(s) or s=='.':
            bl = True
            ns = s+ns
        elif bl:
            break


    return atof(ns)

def getdate_temp(str1):
  if str1 is None :return None
  ns = ''
  for s in str1:
    if is_number(s) or s=='-':
          ns+=s
    
  
  if len(ns)<4:
    ns=''
  elif len(ns)==4:
    ns=str(ns)+'-01-01'
  elif ns.find('-')>0 and len(ns)<8:
    ns=str(ns)+'-01'
  elif ns.find('-')>0:
    pass
  else:
    return None
  
  try:
    
    return datetime.datetime.strptime(ns,'%Y-%m-%d')    
  except Exception,e:
    return None



def atof(s,f=0.0):

    if s is None:s=''
    try:
        _t = float(str(f))
    except ValueError:
        _t = 0
    try:
        return float(s)
    except ValueError:
        return _t

def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar<=u'\u0039':
        return True
    else:
        return False

        
if __name__=='__main__':


    globalDic[u"机构名称"]=1
    globalDic[u"公司名称"]=1
    globalDic[u"企业名称"]=1
    globalDic[u"企业机构名称"]=1

    globalDic[u"公司简介"]=2
    globalDic[u"联系人"]=3

    globalDic[u"公司职务"]=4
    globalDic[u"职务"]=4

    globalDic[u"区号"]=5
    globalDic[u"电话区号"]=5

    globalDic[u"公司电话"]=6
    globalDic[u"电话"]=6
    globalDic[u"联系电话"]=6

    globalDic[u"公司传真"]=7
    globalDic[u"传真"]=7
    globalDic[u"区号传真"]=7

    globalDic[u"公司移动电话"]=8
    globalDic[u"手机"]=8

    globalDic[u"电子邮箱"]=9
    globalDic[u"邮箱"]=9


    globalDic[u"法人代表"]=10
    globalDic[u"法人"]=10
    globalDic[u"负责人"]=10


    globalDic[u"公司地址"]=11
    globalDic[u"地址"]=11
    globalDic[u"住所"]=11
    globalDic[u"企业地址"]=11

    globalDic[u"邮政编码"]=12
    globalDic[u"邮编"]=12
    globalDic[u"公司邮编"]=12


    globalDic[u"经营范围"]=13

    globalDic[u"经营行业"]=14
    globalDic[u"行业名称"]=14


    globalDic[u"企业类型"]=15
    globalDic[u"经济类型"]=15


    globalDic[u"经营模式"]=16


    globalDic[u"注册资金"]=17
    globalDic[u"注册资本"]=17

    globalDic[u"年营业额"]=18
    globalDic[u"营业收入"]=18


    globalDic[u"员工人数"]=19
    globalDic[u"年末人员"]=19
    globalDic[u"人数"]=19


    globalDic[u"成立时间"]=20
    globalDic[u"成立日期"]=20
    globalDic[u"注册日期"]=20
    globalDic[u"成立日期"]=20

    globalDic[u"地区"]=21
    globalDic[u"城市"]=21
    globalDic[u"城市名称"]=21
    globalDic[u"地区2"]=21


    globalDic[u"公司网址"]=23

    #行政区号
    
    conn=MySQLdb.connect(host='10.10.113.1',user='root',passwd='111111',port=3306,db="zi")
    strsql = 'select region_id,Areacode,postcode,MobileNumber from dm_mobile'
    conn.set_character_set('utf8')
    cur = conn.cursor()

    try:
      cur.execute(strsql)
      data =cur.fetchall()
      for a in data:
        if not globalMoblieDic.has_key(a[3].strip()):
          globalMoblieDic[a[3].strip()]=a[0].strip()
        if not globalExtelDic.has_key(a[1].strip()):
          globalExtelDic[a[1].strip()] = a[0].strip()
        if not globalPostDic.has_key(a[2].strip()):
          globalPostDic[a[2].strip()]=a[0].strip()


      del data
    except Exception, e:
      print e
      libes2.writeLog('t_db error,ERROR:'+str(e))
    finally:
      cur.close()
      conn.close()
    
    # input processes
    filepath=u"./2015bzdb/"
    
    GetData(filepath)
    
    #print getdate_temp(u"2005 年")
