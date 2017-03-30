# -*- coding: utf-8 -*- 


import multiprocessing 

import time,datetime
import libes2
import json,io,os,sys,MySQLdb,shutil
import xlrd,uuid,hashlib
import csv,codecs

reload(sys)
sys.setdefaultencoding('utf-8')

this_path = os.path.normpath(os.path.split(os.path.realpath(__file__))[0])
sys.path.append(this_path+'/lib')

from utils import ucsv

from utils import ulog,udate,umysql,ustr,utils
from project import libes2 
        
if __name__=='__main__':

    reader = ucsv.UnicodeReader(open('./org_db_distinct_joined.csv'))
    rlist = []
    i=1
    for line in reader:
        dat = {}
        dat['org_id'] = line[0]
        dat['org_name_cn'] = line[1]
        dat['org_desc'] = line[2]
        dat['uname_contact'] = line[3]
        dat['uposition_contact'] = line[4]
        dat['Extel'] = line[5]
        dat['Tel'] = line[6]
        dat['Fax'] = line[7]
        dat['mobile'] = line[8]
        dat['email'] = line[9]
        dat['uname_holder'] = line[10]
        dat['org_addr_cn'] = line[11]
        dat['postcode'] = line[12]
        dat['org_gov_bzscope'] = line[13]
        dat['ZIIndustryDesc'] = line[14]
        dat['org_gov_type'] = line[15]
        dat['org_gov_bzmode'] = line[16]
        dat['registered_capital'] = line[17]
        dat['org_revenues'] = line[18]
        dat['org_pers_count'] = line[19]
        dat['date_foundation'] = line[20]
        dat['region_temp_str'] = line[21]
        dat['remark'] = ''
        dat['website'] = line[23]
        dat['geo_region_id'] = line[24]

        dat["recommend_brandcats"] = line[25]

        dat["recommend_groups"] = ""
        dat["recommend_groupsx"] = ""
        dat["recommend_patent_class_i13"] = ""

        dat["owned_brandcats"] = line[26]
        dat["owned_groups"] = ""
        dat["owned_groupxs"] = ""
        dat["owned_patent_class_i13"] = ""
        dat["owned_brands"] = line[27]
        dat["owned_patents"] = ""


        rlist.append(dat)
        i+=1
        if i%500==0:
            try:
                libes2.update_to_es_org(rlist)
            except Exception,e:
                print str(e)
            finally:
                print 'handled...'+str(i)
                del rlist[:]


    if len(rlist)>0:
      try:
          libes2.update_to_es_org(rlist)
      except Exception,e:
          print str(e)
      finally:
          print 'handled...last'
          del rlist[:]

        
        
        
    
