# -*- coding: utf-8 -*- 

import logging
from logging.handlers import TimedRotatingFileHandler
from conf import settings
import datetime




logging.basicConfig(level=logging.INFO,               
                datefmt='%a, %d %b %Y %H:%M:%S',
                filemode='w')

format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
formatter = logging.Formatter(format)

file_time_hdler=TimedRotatingFileHandler(settings.COMMON_LOG_FILE,"D",1,0)
file_time_hdler.setFormatter(formatter)
file_time_hdler.suffix="%Y%m%d.log"

#console = logging.StreamHandler()
#console.setFormatter(formatter)
#console.setLevel(logging.INFO)


log1 = logging.getLogger('')
log1.addHandler(file_time_hdler)
#log1.addHandler(console)


def log(str1):
    logging.info(str1)

def writeLog(str1):
    with open(APP_ABS_LOG_PATH+'/logs.txt','ab') as f:
        f.write("LOG:"+datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")+":\r\n"+str1+"\r\n")

def writeDefLog(filepath,str1):
	with open(filepath,'ab') as f:
		f.write("LOG:"+datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")+":\r\n"+str1+"\r\n")

#used for sign lastid then need config.overwirite every time.
def writeLastid(filepath,str1):
    with open(filepath,'w+') as f:
        f.write(str+"\r\n")