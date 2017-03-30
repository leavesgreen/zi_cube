# -*- coding: utf-8 -*- 
import pinyin

#string to int
def atoi(s,d=0):
    if s is None:s= ''

    try:
        _t = int(float(str(d)))
    except ValueError:
        _t = 0
    try:
        return int(float(s))
    except ValueError:
        return _t

#string to float
def atof(s,f=0.0):

    if s is None:s=''
    try:
        _t = float(str(f))
    except ValueError:
        _t = 0
    try:
        return float(s)
    except ValueError:
        return _t


def is_chinese(uchar):

    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False

def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar<=u'\u0039':
        return True
    else:
        return False

def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
        return True
    else:
        return False

def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False


def B2Q(uchar):
    """半角转全角"""
    inside_code=ord(uchar)
    if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
        return uchar
    if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
        inside_code=0x3000
    else:
        inside_code+=0xfee0
    return unichr(inside_code)
 
def Q2B(uchar):
    """全角转半角"""
    inside_code=ord(uchar)
    if inside_code==0x3000:
        inside_code=0x0020
    else:
        inside_code-=0xfee0
    if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
        return uchar
    return unichr(inside_code)


#默认进来的一定是中文,已经过split处理;
def get_pinyin(str1):

    if str1=='':return ''

    list1 =set(str1.split(u' '))

    str2 = ''
    for a in list1:
        
        str2 += pinyin.get(a,u' ')+u' '

    return str2.strip()

#从字符串中获取数字
def get_numbers(str1):
    #
    ns = ''
    for s in str1:
        if is_number(s) or s=='.':
          ns+=s
    return atof(ns)

#用于区间值时,取后面的大值
def get_lastnumbers(str1):
    ns =''
    tl = len(str1)
    bl = False
    for i in range(tl):
        s = str1[tl-i-1]
        if is_number(s) or s=='.':
            bl = True
            ns = s+ns
        elif bl:
            break
    return atof(ns)

def __convert_n_bytes(n, b):
    bits = b*8
    return (n + 2**(bits-1)) % 2**bits - 2**(bits-1)

def __convert_4_bytes(n):
    return __convert_n_bytes(n, 4)

#use as java/net string.Hashcode()
def getHashCode(s):
    h = 0
    n = len(s)
    for i, c in enumerate(s):
        h = h + ord(c)*31**(n-1-i)
    
    return __convert_4_bytes(h)