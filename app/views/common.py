import sys
from django.shortcuts import render,redirect
from pprint import pprint
from django.utils.termcolors import colorize

def debug_exception(e):
    """ Print exception details """

    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = exc_tb.tb_frame.f_code.co_filename
    print(exc_type,'"%s", line %s' % (fname, exc_tb.tb_lineno))
    cprint(e)

def cprint(str_to_print, fg = "white", bg = "blue"):
    print(colorize(str_to_print, fg=fg, bg=bg))

def raise_error(msg):
	raise ValueError(msg)