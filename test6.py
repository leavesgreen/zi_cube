
import multiprocessing 

import time,datetime

import json,io,os,sys,shutil
import uuid,hashlib
import csv,codecs




reload(sys)
sys.setdefaultencoding('utf-8')


this_path = os.path.normpath(os.path.split(os.path.realpath(__file__))[0])
sys.path.append(this_path+'/lib')


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self









def write_to_csv(fpath,line):

    writer = csv.writer(open(fpath,"ab"), delimiter='\t',quoting=csv.QUOTE_NONE)
    try:
      writer.writerow(line)
    except Exception,e:
      print e
    finally:
      #print 'write to csv success...'
      del line

      

if __name__=='__main__':

    #init_redis()
    #sys.exit(0)
    

    reader = csv.reader(codecs.open('d:/temp/temp01.txt','r', 'utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE)

    #reader = UnicodeReader(open('d:/temp/temp01.txt'),dialect=csv.excel,quoting=csv.QUOTE_NONE)

    out_path = 'd:/temp/temp02.txt'

    i=0
    
    for line in reader:
        #print line
        
        

        #print 'handling. line:'+str(i)

        if line is None:
            print 'this line is invalid.....'
            continue

        #print line
        #print len(line)
        
        line[0] = hashlib.md5(line[0]).hexdigest()+str(len(line[0]))
        line[6]=''
        
        #print line

        #for a in line:
            #pass
        #    print a

        write_to_csv(out_path,line)

        print 'finish:'+str(i)
        i+=1
