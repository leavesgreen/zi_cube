# -*- coding: utf-8 -*-
#!/usr/bin/env python
from collections import OrderedDict

class orMapping(object):

    def __init__(self):

        self._field="" #名称;
        self._label="" #显示成什么,当多语言时,这里可以是code,显示时替换;
        self._type="varchar" #类型,int,varchar,text,datetime,double
        self._defaultValue=0
        self._length = 0 #varchar时才有用;
        self._nullable = True

        self._vld = False;  #校验否?无论是否校验,length都得校验;
        self._vldType= "" #required|num|date|email|eng|chs|ip|
        self._vldMsg=""

        self._urCtl = False #控制权限否?
        self._resType="" #所有field统称 model.meta, _field是rescode ; 其余的遵循统一定义,pk的resType与model的resType一致; 但model未必还会有;

        self._fk = False #field是否外键;
        self._fkType = "o2m" #o2o,o2m,m2m
        self._fkFiled = "id" #对方列名;
        self._fkMtbl="" #中间表,当使用m2m时,外键表id建议使用id;
        self._fkLazy=True #延迟加载;
        self._fkMe = "o" #o2m,自己是哪一方?
        self._fkmodel = "Role" #外键的对象实体名称;如果有命名空间呢?据此获取对方表名;
        self._fkAttr = "roles" #在本实体内

        self._ds =None #数据源,如果是单纯选择,[k:v]形式,

class orModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name=='orModel':
            return type.__new__(cls, name, bases, attrs)
        attrs["_mappings"] = OrderedDict()
        a = orMapping();
        a._field="ds_group_id"
        a._label = "编组号"
        attrs["_mappings"][a._field]=a;
        a = orMapping();
        a._field="ds_group_desc"
        a._label = "编组描述"
        attrs["_mappings"][a._field]=a;

        attrs["_tbl"] = "ds_group" #table名
        attrs["_urCtl"] = False
        attrs["_resType"] =""
        attrs["_pk"] = "ds_group_id"


        return type.__new__(cls, name, bases, attrs)

class orModel(dict):
    __metaclass__ = orModelMetaclass
    _mappings = {} #mapping可以从数据库加载; cls配置;
    _tbl = "" #table名
    _urCtl = False
    _resType = ""
    _pk = ""
    _cachesql={}

    def __init__(self,**kw):
        super(Model, self).__init__(**kw)
        self["__mappingDic__"] = {} #该字典用于判lazy的谁加载了,谁没加载;

    def __getattr__(self,key): #以字典存储,对每个fields; 对于lazy加载的对象,自动赋值None;使用时加载;
        try:
            return self[key] #when lazy and not load before? try load;
        except KeyError:
            raise AttributeError(r"'orModel' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getselsql(self):
        pass

    def getuptdsql(self):
        pass

    def getinssql():
        pass

    def getdelsql():
        pass

    def get(self,sqlWhere,**kwgs):
        pass
        #生成sql

    def getAll(self,sqlWhere,**kwgs):
        pass

    def update(self):
        pass

    def insert(self):
        fields = []
        params = []
        args = []
        for k, v in self._mappings.iteritems():
            fields.append(k)
            params.append('?')
            args.append(getattr(self,k))

        sql = 'insert into %s (%s) values (%s)' % (orModel._tbl, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))



class ds_group(orModel):


    def __init__(self):
        pass



if __name__=='__main__':
    a = ds_group();
    a.ds_group_id = "10"
    a.ds_group_desc = "20"
    a.insert();
