# uname.py

__version__ = '1.0.0' # Major.Minor.Patch

import os


def __main__(args):
    uname = os.uname()
    print ("System {} release {} version {}".format(uname.sysname, uname.release, uname.version))
    print ("Machine type {}".format(uname.machine))


