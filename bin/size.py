# size.py

__version__ = '1.0.0' # Major.Minor.Patch

from sh import human
import os
from machine import Pin, PWM
from utime import sleep


def __main__(args):
    if len(args) > 2:
        #sz=os.path.getsize(args[2])
        #sz = os.stat(args[2]).st_size    # AttributeError: 'tuple' object has no attribute 'st_size'
        sz = os.stat(args[2])[6]    # (32768, 0, 0, 0, 0, 0, 4604, 106, 106, 106)
        #print(sz)

        blk=float(sz+4095)
        blocks=int(blk/4096)
        space=4096*blocks

        if len(args) > 3:
            print("{}\t{}\t{}".format(sz,space,args[2]))
        else:
            print(sz)
    else:
        print("Usage: size filename.ext [1]")
