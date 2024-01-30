# fbtest.py

__version__ = '1.0.0' # Major.Minor.Patch

from sh import human
import os
import machine
import time
import framebuf

def __main__(args): # python filename paramaters...
    xmax=320
    ymax=240
    cdepth=2
    if len(args) > 2:
        xmax = int(args[2])
    if len(args) > 3:
        ymax = int(args[3])
    if len(args) > 4:
        cdepth = float(args[4])
    if len(args) > 5:
        another = float(args[5])

    print("{}: xmax{} ymax{} cdepth{}".format(args[1], xmax, ymax, cdepth))
    # FrameBuffer needs 2 bytes for every RGB565 pixel
    
    fbuf = framebuf.FrameBuffer(bytearray(xmax * ymax * 2), xmax, ymax, framebuf.RGB565)
    fbuf.fill(0)
    fbuf.text('MicroPython!', 0, 0, 0xffff)
    fbuf.hline(0, 9, 96, 0xffff)
