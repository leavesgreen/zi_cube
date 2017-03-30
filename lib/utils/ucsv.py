# -*- coding: utf-8 -*- 
import csv,codecs
import ulog



#use as for line in reader:
def get_unicode_reader(filepath):
    reader1 = UnicodeReader(open(filepath))
    return reader1

def get_reader(filepath):
    reader1 = csv.reader(open(filepath))
    return reader1


def write_lines(filepath,lines):
    writer = csv.writer(open(filepath,"ab"),quoting=csv.QUOTE_ALL)
    try:
        writer.writerows(lines)
    except Exception,e:
        ulog.log('insert db error:,ERROR:'+str(e))
    finally:
        ulog.log('write to csv success...lines done:'+str(len(lines)))


def write_line(filepath,line):
    writer = csv.writer(open(filepath,"ab"),quoting=csv.QUOTE_ALL)
    try:
        writer.writerow(line)
    except Exception,e:
        ulog.log('insert db error:,ERROR:'+str(e))
    finally:
        pass
        #ulog.log('write to csv success...lines done:'+str(len(line)))


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

