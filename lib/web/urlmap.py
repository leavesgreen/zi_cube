# -*- coding: utf-8 -*-

class Urlmap(object):
    def __init__(self):
        self.handlers = []

    def __call__(self, url, **kwds):
        def _a(cls):
            self.handlers.append((url, cls, kwds))
            print cls
            return cls
        return _a


def urlHandlers(*args):
    handlers = []
    for i in args:
        handlers.extend(i.urlmap.handlers)
    return handlers

urlmap = Urlmap()




if __name__=='__main__':
    print tuple(urlmap.handlers)