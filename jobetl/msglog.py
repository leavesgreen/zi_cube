# coding=utf8


from pytz import utc

from apscheduler.schedulers.blocking import BlockingScheduler

import time
import datetime, httplib2, copy, json
import entitys.msg_base as db
from entitys.msg_entitys import msglog, msgcache, msgsentlog





def get_msgs():
    # try
    #这里改为只有一个发送message的任务,放在内网,当有一段连接失败时,取不到最新的日志,但是不影响发送历史中的cache信息;

    http = httplib2.Http()
    http.add_credentials('admin', 'B8vEK*UR')
    url = 'http://123.57.95.46:15672/api/queues/'
    headers = {'content-type': 'text/plain'}

    response, content = http.request(url, 'GET', headers=headers, body=None)

    return content


def get_msgcache_by_msg(m, itype):
    if m is None:
        return None
    return msgcache(key=m.vhost + '.' + m.queue + "." + str(itype), msg_pub=m.msg_pub, msg_in=m.msg_in, msg_left=m.msg_left, msg_out=m.msg_out, itype=itype)



def send_message(msg):
    http = httplib2.Http()
    http.add_credentials('admin', 'B8vEK*UR')
    url = 'http://114.255.71.158:8061/?username=***&password=***&message=%s&phone=13910123456&epid=111&linkid=&subcode=' % msg
    headers = {'content-type': 'text/plain'}

    response, content = http.request(url, 'GET', headers=headers, body=None)

    if content==0:
        pass
        #log success.
        return  True



# get msg from rabbitmq

def main():
    dbsession = db.get_session()

    log_msgs = []  # 本次取到的记录;

    # 以下需要测试
    # publish:count of message published. 貌似是总数
    # messages: 留存的message, 还留着的;
    # ack:已确认发出的,
    # vhost:
    # name:queues

    bl_need_send = False  # 是否发送
    msgsent_log = []  # 发送历史记录;
    lastmsg_cache_dic = {}  # lastmsgs should get from cache
    msg_cache_new = []  # 需要新增的

    d_now = datetime.datetime.now()

    content = get_msgs()

    for a in json.loads(content):

        print '-------------------------------------------------'

        m = msglog(vhost=a["vhost"], queue=a["name"])

        m.id = d_now.strftime('%Y%m%d%H%M%S') + '.' + m.vhost + '.' + m.queue

        m.msg_left = a["messages"]  # message

        if a.has_key("message_stats"):
            m.msg_out = a["message_stats"].get("ack",0)  # ack
            m.msg_pub = a["message_stats"].get("publish",0) # publish

        print 'm......' + str(m.msg_out)

        print 'm......' + str(m.is_new)

        m.msg_in = m.msg_pub - m.msg_left - m.msg_out
        m.time_update = d_now

        log_msgs.append(m)


    if lastmsg_cache_dic is None or len(lastmsg_cache_dic) == 0:
        # 取得last
        msgcaches = dbsession.query(msgcache).all()

    for m in msgcaches:
        lastmsg_cache_dic[m.key] = m

    for m in log_msgs:

        _key = m.vhost + '.' + m.queue

        _key_log = _key + '.1'  # log 1
        _key_send = _key + '.0'  # send 0

        msg_send_add = get_msgcache_by_msg(m, 0)  # 本期增加的发送数;
        msg_log_cache = get_msgcache_by_msg(m,1) #本期取得的message,log; 根据msglog直接生成就行

        if not lastmsg_cache_dic.has_key(_key_log):
            if m.msg_pub > 0:
                msg_cache_new.append(msg_log_cache)
        else:
            if m.msg_pub < lastmsg_cache_dic[_key_log].msg_pub:  # 说明可能重启过;现有的msg_send_add就是新增的部分;
                bl_need_send = True
            else:
                c1 = lastmsg_cache_dic[_key_log]

                msg_send_add.msg_pub = msg_send_add.msg_pub - c1.msg_pub
                msg_send_add.msg_in = msg_send_add.msg_in - c1.msg_in
                msg_send_add.msg_left = msg_send_add.msg_left
                msg_send_add.msg_out = msg_send_add.msg_out - c1.msg_out



        if msg_send_add.msg_pub > 0:
            if not lastmsg_cache_dic.has_key(_key_send):
                msg_cache_new.append(msg_send_add)
            else:
                c0 = lastmsg_cache_dic[_key_send]
                c0.msg_pub = c0.msg_pub + msg_send_add.msg_pub
                c0.msg_in = c0.msg_in + msg_send_add.msg_in
                c0.msg_pub = c0.msg_out + msg_send_add.msg_out
                c0.msg_left = msg_send_add.msg_left

                lastmsg_cache_dic[_key_send] = c0

        # save to db;

        # judge need send or not. need override
        #always run every 1 minutes.but only send on 30. or 0.

    if not bl_need_send:
        #如果当前在0,30分的,1分钟区间内;执行send
        if (d_now.minute==59 and d_now.second>30) or (d_now.minute==1 and d_now.second<=30):
            #整点发送
            bl_need_send = True
        elif (d_now.minute==29 and d_now.second>30) or (d_now.minute==30 and d_now.second<=30):
            bl_need_send = True



    if bl_need_send:

        # send msg:
        tempstr = ''  # only for test.

        temp_caches = msg_cache_new + lastmsg_cache_dic.values()

        for a in temp_caches:

            if a.itype == 1: continue
            if (a.msg_pub ==0 and a.msg_out==0 and a.msg_in==0 and a.msg_left ==0) : continue


            tempstr += '\r' + str(a.msg_left)

            b = msgsentlog(key=d_now.strftime('%Y%m%d%H%M%S') + '.' + a.key, msg_pub=a.msg_pub, msg_left=a.msg_left,\
                           msg_in=a.msg_in, msg_out=a.msg_out)
            b.time_send = d_now

            msgsent_log.append(b)

        del temp_caches

        for k in lastmsg_cache_dic.keys():
            if lastmsg_cache_dic[k].itype == 1: continue
            if (a.msg_pub ==0 and a.msg_out==0 and a.msg_in==0 and a.msg_left ==0) : continue

            lastmsg_cache_dic[k] = msgcache(key=lastmsg_cache_dic[k].key, itype=0)

        for a in msg_cache_new:
            if a.itype == 1: continue

            a.msg_pub = 0
            a.msg_left =a.msg_left
            a.msg_in=0
            a.msg_out=0



        print 'sent ...............' + tempstr

    # save()

    # 删除所有cache数据;

    dbsession.add_all(log_msgs)
    dbsession.add_all(msgsent_log)



    #dbsession.add_all(msg_cache_new)

    for a in msg_cache_new:
        dbsession.merge(a)
    #
    for a  in lastmsg_cache_dic.values():
        dbsession.merge(a)



    dbsession.commit()

    dbsession.close()





if __name__ == '__main__':


    scheduler=BlockingScheduler()
    scheduler.add_job(main, 'interval', minutes=1)
    scheduler.start()

    #main()

    #db.createdb()



# m1=msglog(id= int(datetime.datetime.now()),msg_in_accum=10,msg_out_accum=20,msg_left=30,time_update=datetime.datetime.now())
# dbsession.add(m1)
# dbsession.commit()
