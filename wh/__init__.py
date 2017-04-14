import time
from splitparser import rend
from pager import render_pager

def datef(d,f):
    return time.strftime(f, time.localtime(int(d)))

def dateg(d,f):
    return time.strftime(f, time.gmtime(int(d)))
