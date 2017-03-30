# -*- coding: utf-8 -*-
#!/usr/bin/env python
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps

import os.path
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web,sys


import  json,MySQLdb,io,uuid,shutil
import traceback,StringIO,urllib2,cStringIO

from datetime import datetime,timedelta
from dateutil import relativedelta
import calendar as calendar
import tornado.process
import time


from tornado.options import define, options




reload(sys)
sys.setdefaultencoding('utf-8')


this_path = os.path.normpath(os.path.split(os.path.realpath(__file__))[0])
sys.path.append(this_path+'/lib')



from utils import ulog,udate,umysql,ustr,utils
from utils.cache import miniCache as mcache
from project import ipdss_sales as ipdss
import asyncMysql as ams

#from task_redis import add

STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")
EXECUTOR = ThreadPoolExecutor(max_workers=4)


class stdsend(object):

    pass;

class stdresp(object):
    pass;

class ziException(Exception):
    """docstring for ClassName"""
    def __init__(self,errcode,errmsg):
        self.errcode = errcode
        self.errmsg = errmsg


def unblock(f):

    @tornado.web.asynchronous
    @wraps(f)
    def wrapper(*args, **kwargs):
        self = args[0]

        def callback(future):
            self.write(future.result())
            self.finish()

        EXECUTOR.submit(
            partial(f, *args, **kwargs)
        ).add_done_callback(
            lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                partial(callback, future)))

    return wrapper


class JustNowHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("i hope just now see you")


class SleepHandler(tornado.web.RequestHandler):

    @unblock
    def get(self, n):
        time.sleep(float(n))
        return "Awake! %s" % time.time()


class SleepAsyncHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self, n):

        def callback(future):
            self.write(future.result())
            self.finish()

        EXECUTOR.submit(
            partial(self.get_, n)
        ).add_done_callback(
            lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                partial(callback, future)))

    def get_(self, n):
        time.sleep(float(n))
        return "Awake! %s" % time.time()



class BaseHandler(tornado.web.RequestHandler):


    def check_user(self):
        tempuser = self.get_argument('crm3u',None);

        if tempuser is None:
            tempuser = self.get_secure_cookie("user")
        else:
            self.set_secure_cookie("user",tempuser) #目前仅针对crm3用户;

        if tempuser is None:
            raise  ziException('0x101','no logined user found');

            #tempuser = str(uuid.uuid1())
            #self.set_secure_cookie("user",tempuser)
            #若未给定user参数,u=??,user为空; 对于为空的user,使用其他cookie值;
            #这里的cookie值不同于用户在stdsend中发送的cookie值;彼处的cookie为其他宿主网站的cookie; 在网站自身的应用中,这两个暂且相等;
        print "crm3u."+tempuser

        return tempuser


    def write_error(self,status_code,**kwargs):
        self.set_status(200)
        self.set_header("Content-Type", "application/json")
        #print exc_info
        #print 'new error..........'
        stdresp = {}
        stdresp["status"]=0

        if  isinstance (kwargs["exc_info"][1], ziException):
            stdresp["errcode"]=kwargs["exc_info"][1].errcode
            stdresp["errmsg"]=kwargs["exc_info"][1].errmsg
        else:
            stdresp["errcode"]=status_code
            stdresp["errmsg"]=str(kwargs["exc_info"][1])

        stdresp["stdmsg"] = stdresp["errmsg"]

        resp ={}
        resp["stdresp"] = stdresp



        #utils.log(json.dumps(resp))

        #print traceback.format_exception(kwargs["exc_info"][0],kwargs["exc_info"][1],kwargs["exc_info"][2]) #use to export the traceback.

        #print str(kwargs["exc_info"][1]) #use to print the exception,and exception should use json code; when is not the base exception of user define.judge it.

        self.write(json.dumps(resp))

        self.finish()




class Users(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        # 参数通过args的list传递，回调通过callback指定
        #add.apply_async(args=[4,4], callback=self.on_success)
        pass
    def on_success(self, response):
        # 获取返回的结果
        users = response.result
        print users

        self.write(str(users))
        self.finish()







class MainHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self,rptId):
        #datas=yield  ams.test()
        #print datas
        #self.write(json.dumps(datas))
        #self.finish()

        self.render('index4.html',tempuser="aaaa");
        self.finish();
        
class MainHandler2(BaseHandler):

    def get(self,rptId):
        #tempuser =super(MainHandler,self).check_user();
        #self.write("bbbbbbbbbbbbbbbbbbbbbbbb"+rptId)
        self.redirect('https://gss1.bdstatic.com/5eN1dDebRNRTm2_p8IuM_a/res/r/image/2016-10-24/5b2055c5db28207a7b6110da0c1b0d6c.jpg')



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/m1/(.*)", MainHandler),
            (r"/m2/(.*)", MainHandler2),
            (r"/justnow", JustNowHandler),
            (r"/sleep/(\d+)", SleepHandler),
            (r"/sleep_async/(\d+)", SleepAsyncHandler),

        ]
        settings = dict(
            AppTitle='app names',
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RAgaegjaej32NDOM_VALUE_HERE__",
            static_path=STATIC_PATH,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            login_url='/login',
            ui_modules={},
            xsrf_cookies=True,
            debug=True,
            autoescape=None,
        )
        self.db = None #the db use in page.
        #tornado.locale.load_translations('i18n')
        #tornado.ioloop.PeriodicCallback(self._ping_db, 4 * 3600 * 1000).start()
        #ipdss.refreshCache()
        tornado.web.Application.__init__(self, handlers, **settings)




define("port", default=8889, help="run on the given port", type=int)
define("define_some_var", default="001", help="define_some_var:001")





def main():

    tornado.options.parse_command_line()

    print options.port
    print options.define_some_var

    http_server = tornado.httpserver.HTTPServer(Application())

    #on windows, and single process;

    http_server.listen(options.port)

    #on linux,multi process,with debug =false
    #http_server.bind(options.port)
    #http_server.start(num_processes=2)


    #start
    tornado.ioloop.IOLoop.instance().start()


    #cache



if __name__ == "__main__":
    main()
