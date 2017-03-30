# -*- coding: utf-8 -*- 

import os.path
from elasticsearch import Elasticsearch
import pinyin,json,random,csv   
from datetime import datetime
from datetime import date
from datetime import timedelta
from sqlalchemy.ext.declarative import DeclarativeMeta

import ustr

def get_pinyin_bylist(ls):
    if len(ls)==0:return ''

    str1 = ''
    bl_space = True
    for a in ls:
        if a[1]==3:
            str1+=pinyin.get(a[0],u' ') #增加对于拼音的分空格处理;
        elif a[1]==2:
            if not bl_space:
                str1+=u' '
            str1+=a[0]+u' '
        else:
            if a[0]==u' ':
                str1=str1.strip()+','
        
        bl_space = False
        if a[0]==u' ':
            bl_space = True


    #这里到底该不该加"",存疑;不加使用or有问题;加了查询模糊拼音有问题;
    #return u'"' +u'" OR "'.join(str1.split(',')) +'"'
    return u' '.join(str1.split(',')) 

def get_trans_by_cn(str1):
    return str1

def get_trans_by_en(str1):
    return str1

#默认进来的一定是中文,已经过split处理;
def get_shapelike(str1):

    #str1打散成中文;
    wds = tuple(str1)

    wds2 = []
        
    for a in wds:
        if not a==u' ': #注意可能会造成不连贯;
            ls1= [a]
            a1 = Shapelikes.get_words(a) 
            if a1 is not None:
                ls1.extend(list(a1))

            wds2.append(ls1)
        else:
            wds2.append([a])

    #取10个:
    #print json.dumps(wds2)

    i=0
    rset = set()

    while i<10:
        _str = ''
        for ls1 in wds2:
            _str+=random.choice(ls1)

        rset.add(_str)
        i+=1

    
    #print rset
    return rset



class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)     # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:    # 添加了对datetime的处理
                    if isinstance(data, datetime):
                        fields[field] =data.strftime('%Y-%m-%d %H:%M:%S')
                    elif isinstance(data, date):
                        fields[field] = data.strftime('%Y-%m-%d')
                    elif isinstance(data, timedelta):
                        fields[field] = (datetime.min + data).time().isoformat()
                    else:
                        fields[field] = None
            # a json-encodable dict
            return fields
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class Shapelikes:
    
    _wordsDic = {}
    @classmethod
    def initData(cls):

        if len(cls._wordsDic.keys())>0:
            return

        k = 1
        with open("resource/old.csv") as csvfile:
            reader = csv.reader(csvfile)   
            for line in reader:
                if line[0]=='':
                    k+=1
                    continue
                cls._wordsDic[ unicode(line[0].strip(),'utf-8') ] = unicode(line[4].strip(),'utf-8')

                '''
                k+=1
                if k>3:
                    break
                '''
            csvfile.close()


    @classmethod
    def get_words(cls,str1):
        return cls._wordsDic.get(str1,None)

def splitwords2(str1): 
    #返回list,按原顺序返回,保留空格,如果有

    rlist =[]
    if str1=='':return rlist

    list1 =tuple(str1)

    bl_lst = 0
    bl_this = 0
    
    str2 =''

    for a in list1:

        if a ==u' ': 
            bl_this =0
        elif ustr.is_number(a):
            bl_this = 1
        elif ustr.is_alphabet(a):
            bl_this = 2
        elif ustr.is_chinese(a):
            bl_this = 3
        else:
            bl_this = 4
        
        if bl_this==bl_lst:
            if bl_this <> 0:
                str2+=a
        else:
            if not str2=='':
                rlist.append((str2,bl_lst))


            str2=''
            if bl_this <> 0:
                str2+=a
            else:
                rlist.append((u' ',bl_this))


        bl_lst = bl_this

    if str2.strip()<>'':

         rlist.append((str2,bl_lst))


    return rlist

def splitwords(str1):
    #返回dic,按空格,中,英文,数字,拆分开; {1:str}#0空格,1数字,2英文,3中文,4其他,其他直接忽略;
    #必须是unicode

    rdic ={}
    if str1=='':return rdic

    list1 =tuple(str1)

    bl_lst = 0
    bl_this = 0
    
    str2 =''

    for a in list1:

        if a ==u' ': 
            bl_this =0
        elif ustr.is_number(a):
            bl_this = 1
        elif ustr.is_alphabet(a):
            bl_this = 2
        elif ustr.is_chinese(a):
            bl_this = 3
        else:
            bl_this = 4
        
        if bl_this==bl_lst:
            if bl_this <> 0:
                str2+=a
        else:
            rdic[bl_lst]=rdic.get(bl_lst,'')+str2 + u' '
            str2=''
            if bl_this <> 0:
                str2+=a
        bl_lst = bl_this

    if str2.strip()<>'':
        rdic[bl_lst]=rdic.get(bl_lst,'')+str2 + u' '


    #去除重复
    for k in rdic:
        rdic[k] =u' '.join(set(rdic[k].split(u' ')))

    return rdic





STATUS_DIC ={
    '1': {'is_invalid':False,'date_exclusive_begin':False},
    '2': {'is_invalid':False,'date_pre_pub':True,'date_exclusive_begin':False},
    '3': {'is_invalid':False,'date_exclusive_begin':True,'date_exclusive_end':True},
    '4': {'is_invalid':True,'date_exclusive_begin':False},
    '5': {'is_invalid':True,'date_exclusive_begin':True,'date_exclusive_end':True}
}


def get_union_status(status_list):

    t1 = []
    for _s in status_list:
        _stat  = STATUS_DIC.get(_s)

        if _stat is not None:
            t1.append(_stat)

    #print t1

    lasta = None
    for a in t1:
        if lasta is None:
            lasta = a
        else:
            lasta = union_status(lasta,a)
            
    return lasta


def union_status(a,b):
    #F,F->F; T,T->T; T,F->N; N,* ->N     
    print a
    print b

    t = {}
    if len(a)==0 or len(b)==0:
        return t;

    for k in a.keys():
        if a[k]==False and b.get(k)==False:
            t[k]=False
        elif a[k]==True and b.get(k)==True:
            t[k]=True
            
    return t


def ArrayToData(arr1,idata,ilgd=None,ix=None):
    '''
    返回类型,
    Lengend list,即分组维度;
    Axis,轴维度; list,轴维度;
    Datas,数据;组数与lengend的长度一致;数据组里面与Axis的长度一致,Axis没有,或为1时,应该为单个值;
    '''
    
    dic = {}
    _lengends = set();
    _axis = set();
    _datascount = {}; #改成对象就好了;
    _datassum = {};

    #先获取所有key,并排序;
    for x in arr1:
        _l = 'NA' if ilgd is None else str(x[ilgd]);
        _a = 'NA' if ix is None else str(x[ix])

        _lengends.add(_l);
        _axis.add(_a);

        #理论上可累加,计数和求和等;
        _datascount[_l+'.'+_a]=_datascount.get(_l+'.'+_a,0)+1
        _datassum[_l+'.'+_a]=_datassum.get(_l+'.'+_a,0)+float(x[idata])

    dls = [] #sum
    dlc = [] #count

    #排序
    _lengends_ls = list(_lengends);
    _axis_ls = list(_axis);

    _lengends_ls.sort()
    _axis_ls.sort()

    for _l in _lengends_ls:
        dlc1=[]
        dls1=[]
        for _a in _axis_ls:
            dls1.append(_datassum.get(_l+'.'+_a,0));
            dlc1.append(_datascount.get(_l+'.'+_a,0));
        dls.append(dls1)
        dlc.append(dlc1)


    dic["lengend"]=_lengends_ls;
    dic["axis"]=_axis_ls;
    dic["data.sum"]=dls;
    dic["data.count"]=dlc;


    #print json.dumps(dic).decode('unicode-escape');

    return dic["lengend"],dic["axis"],dic["data.sum"],dic["data.count"]

#ck不能重复;list,父亲键,子键 ;;will返回父-子-子-子,父-子,这样的结构;
def get_PrtChd_list(ls1,pk,ck):

    ls2 = []
    if ls1 is None:
        return ls1

    pdic = {}
    dic = {}
    for t in ls1:
        if not pdic.has_key(t[pk]):
            pdic[t[pk]] = []
        pdic[t[pk]].append(t)
        dic[t[ck]]= t

    #查找根节点,即pk在ck中不存在的节点;
    ls_rtk =[x for x in pdic.keys() if not dic.has_key(x)]

    for rtk in ls_rtk:
        __get_PrtChd_list(ls2,rtk,ck,pdic)

    return ls2

def __get_PrtChd_list(ls2,rtk,ck,pdic):
    #print rtk
    #print ls2

    if pdic.has_key(rtk):
        for chd in pdic[rtk]:
            ls2.append(chd)
            __get_PrtChd_list(ls2,chd[ck],ck,pdic)



if __name__=='__main__':
    
    '''
    Shapelikes.initData()
    
    print len(Shapelikes._wordsDic.keys())
    '''
    '''
    s = u'疯'
    print repr(s)
    print repr(Shapelikes._wordsDic.keys()[2])
    print repr(Shapelikes.get_words(s))
    #print tuple(s)
    '''

    '''
    s = u'疯那dgag  遥远 1212的gg   ad 3山4 gggg dd村'
    #s = u'的德大噶'

    a = splitwords2(s)
    print a
    print get_pinyin_bylist(a)
    #print repr(get_shapelike(a[3]))
    #print get_pinyin(a.get(3))

    '''
    print get_union_status(['1','2','3'])
    
