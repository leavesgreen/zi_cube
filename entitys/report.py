# -*- coding: utf-8 -*- 

import os.path

import sys,uuid

from datetime import datetime,date,timedelta

import logging

import utils.utils


class connection(object):
		
	def __init__(self,**kwargs):

		self.id = kwargs.get("id",str(uuid.uuid4()))
		self.name = kwargs.get("name","new connection") 
		self.type =kwargs.get("type","zi-dcs") #type:zi-dcs;(rdbms-mysql/mssql/oracle;weburl;file-txt/csv/json/parquet;bigdata-etc);
		
		self.connstr = kwargs.get("connstr","") #不包括acc,pass,理论上;
		self.account = kwargs.get("account","")
		self.password =kwargs.get("password","")


	@classmethod
	def get_by_dic(cls,dic):
		return connection(**dic)

	@classmethod
	def get_by_db(cls,id):

		return connection(None)





class datasource(object):

	def __init__(self,**kwargs):
		self.id = kwargs.get("id",str(uuid.uuid4()))
		self.name = kwargs.get("name","new datasource")
		self.type = kwargs.get("type","conn") #type:conn; static; js; #conn必须有connection对象,datasource使用其连接; static使用静态数据,在data中指定,指定数据为[]; js定义的半动态数据,生成格式为data格式;
		self.conn = kwargs.get("conn","0")

		self.qsl = kwargs.get("qsl","")
		self.data =  kwargs.get("data") #dict direct set value when static

	def update_data(self):
		if self.type=='static':
			return

		pass #获取数据的方法;


		#head: {name:xxx,vdype:xxx,dimtype:xxx} #field列名,dtype:数据类型;dimtype:维度类型;由olap指定或推断; 无列名式,推断F0-FN;
		#body:[] #2维表格;
	


class params(object):

	def __init__(self,**kwargs):


		self.id = kwargs.get("id",str(uuid.uuid4()))
		self.name = kwargs.get("name","new params")
		self.dtype = kwargs.get("dtype","conn") #type:conn; static; js; #conn必须有connection对象,datasource使用其连接; static使用静态数据,在data中指定,指定数据为[]; js定义的半动态数据,生成格式为data格式;
		self.datasource = kwargs.get("datasource","0")
		self.value = kwargs.get("value")
		self.display =  kwargs.get("display") #dict direct set value when static



	def get_data(self):
		pass #获取数据的方法;


class chartbase(object):
	
	def __init__(self,**kwargs):
		self.id = kwargs.get("id",str(uuid.uuid4()))
		self.title = kwargs.get("title","")
		self.subtitle = kwargs.get("subtitle","")
		self.dimscount = kwargs.get("dimscount",1)
		self.charttype = kwargs.get("charttype",'grid') #the same with report chart type.
		self.options = kwargs.get("options",None)
	
	


class chart(chartbase):

	def __init__(self,**kwargs):
		super(chart,self).__init__(**kwargs)
		


class linechart(chart):
	pass

	



	

class report(object):

	def __init__(self):
		pass

	


if __name__=="__main__":
	pass







'''


'''