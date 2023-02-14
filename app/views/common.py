import json
import sys

from django.utils.termcolors import colorize


def debug_exception(e):
    """Print exception details"""

    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = exc_tb.tb_frame.f_code.co_filename
    print(exc_type, '"%s", line %s' % (fname, exc_tb.tb_lineno))
    cprint(e)


def cprint(str_to_print, fg="white", bg="blue"):
    print(colorize(str_to_print, fg=fg, bg=bg))


def raise_error(msg):
    raise ValueError(msg)


def beautify_form_errors(errors):
    err_msg = ""
    errs = json.loads(errors.as_json())
    for i in errs:
        err_msg += errs[i][0]["message"] + " "

    return err_msg
