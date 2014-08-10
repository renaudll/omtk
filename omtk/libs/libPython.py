import os, types, imp, logging, re
logging = logging.getLogger('libPython')
logging.setLevel(0)

def does_module_exist(module_name):
    try:
        imp.find_module(module_name)
        return True
    except ImportError:
        return False

# src: http://code.activestate.com/recipes/66472/
def frange(start, end=None, inc=None):
    "A range function, that does accept float increments..."

    if end == None:
        end = start + 0.0
        start = 0.0

    if inc == None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)

    return L