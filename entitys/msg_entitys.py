#coding=utf8
__author__ = 'alex'

from sqlalchemy import Column, Integer, String,DateTime
import entitys.msg_base as db


class msglog(db.Base):
	__tablename__ = "msglog"

	id=Column(String(100),primary_key=True)

	vhost=Column(String(100))
	queue = Column(String(100))

	msg_pub = Column(Integer,default=0) #total
	msg_in = Column(Integer,default=0)
	msg_out = Column(Integer,default=0)
	msg_left = Column(Integer,default=0)

	time_update = Column(DateTime)

	def __init__(self,*args,**kwargs):
		self.is_new=0
		self.msg_out = 0
		self.msg_pub = 0

		#if not kwargs.has_key("msg_pub"):
			#kwargs["msg_pub"] = 0
		#if not kwargs.has_key("msg_out"):
		#	kwargs["msg_out"] = 0

		super(msglog,self).__init__(*args,**kwargs)


class msgcache(db.Base):
	__tablename__="msgcache"

	key = Column(String(100),primary_key=True)

	msg_pub =Column(Integer,default=0)
	msg_in = Column(Integer,default=0)
	msg_out = Column(Integer,default=0)
	msg_left = Column(Integer,default=0)

	itype = Column(Integer) #0,1 ; 0 for send; 1 for accum

	time_send = Column(DateTime) #no use

	def __init__(self,*args,**kwargs):
		self.is_new=0
		self.msg_out = 0
		self.msg_pub = 0

		#if not kwargs.has_key("msg_pub"):
			#kwargs["msg_pub"] = 0
		#if not kwargs.has_key("msg_out"):
		#	kwargs["msg_out"] = 0

		super(msgcache,self).__init__(*args,**kwargs)

class msgsentlog(db.Base):

	__tablename__="msgsentlog"

	key = Column(String(100),primary_key=True)

	msg_pub =Column(Integer,default=0)
	msg_in = Column(Integer,default=0)
	msg_out = Column(Integer,default=0)
	msg_left = Column(Integer,default=0)

	#type = Column(Integer) #0,1 ; 0 for send; 1 for accum

	time_send = Column(DateTime)
