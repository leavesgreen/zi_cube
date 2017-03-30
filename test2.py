# -*- coding: utf-8 -*-
#!/usr/bin/env python

from functools import wraps

def my_decorator(func):
    @wraps(func)

    def wrapper(*args, **kwargs):

        print('Calling decorated function...')

        return func(*args, **kwargs)

    return wrapper

@my_decorator('11111')
def example(aa):

    """Docstring"""

    print('Called example function')
    print('the args is '+aa)

print(example.__name__, example.__doc__)

example('ffffffffffffffff')
