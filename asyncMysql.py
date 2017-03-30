# -*- coding: utf-8 -*-
#!/usr/bin/env python

from tornado.ioloop import IOLoop
from tornado import gen
from tornado.concurrent import Future
import tormysql
import uuid

pool = tormysql.ConnectionPool(
    max_connections = 20, #max open connections
    idle_seconds = 7200, #conntion idle timeout time, 0 is not timeout
    wait_connection_timeout = 3, #wait connection timeout
    host = "127.0.0.1",
    user = "root",
    passwd = "000000",
    db = "zi",
    charset = "utf8"
)


@gen.coroutine
def test():
    with (yield pool.Connection()) as conn:
        try:
            with conn.cursor() as cursor:
                yield cursor.execute("INSERT INTO ds_group VALUES('"+str(uuid.uuid1())+"','123','1')")
        except:
            yield conn.rollback()
        else:
            yield conn.commit()

        t=0
        for a in xrange(0,100000000):
            t+=a 

        datas=None
        with conn.cursor() as cursor:
            yield cursor.execute("SELECT * FROM ds_group")
            datas = cursor.fetchall()

    yield pool.close()
    raise gen.Return(datas)
