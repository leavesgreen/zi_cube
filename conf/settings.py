# -*- coding: utf-8 -*- 
import os

APP_ABS_ROOT_PATH = os.path.normpath(os.path.split(os.path.realpath(__file__))[0]+'./..')
APP_ABS_LOG_PATH = APP_ABS_ROOT_PATH+"/logs"
#define keyvalue setting;


#define db
CONN_MYSQL_PAST_ZI_BI = {'host':'10.10.107.4','user':'root','passwd':'000000', 'port':3306, 'db':"zi"}
CONN_MYSQL_BRAND_YUHAN_SRC = {'host':'10.10.100.31','user':'brandreader','passwd':'4t9scAG7', 'port':3306, 'db':"trademark"}


#define es


#log

COMMON_LOG_FILE=APP_ABS_LOG_PATH+"/myapp.log"