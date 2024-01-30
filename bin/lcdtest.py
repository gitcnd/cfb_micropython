# lcdtest.py

__version__ = '1.0.1' # Major.Minor.Patch

# methods:-
#
# ILI9341(self, spi, cs, dc, rst, w, h, r)
# color565(r, g, b)    set_color(fg,bg)    set_pos(x,y)        reset_scroll()
# set_font(font)       init()            reset()
# pixel(x,y,color=_A)  fill_rectangle(x,y,w,h,color=_A)
# erase()              blit(bitbuff,x,y,w,h)
# chars(str,x,y)       scroll(dy)        next_line(cury,char_h)
# write(text):         print(text)

# ARGV=[3];exec(open('bin/lcdtest.py').read())

# from sh import human
import os
import time

from ili934xnew import ILI9341, color565
from machine import Pin, SPI
import m5stack
import glcdfont
import tt14
import tt24
import tt32

dx=320
dy=240
dxm=int(dx/2)
dym=int(dy/2)

def __main__(args):
    run(args[1:])    # mipyshell first 2 arguments are "python" and "blink.py"

def run(args): # ['python', '/bin/set.py', '33', '0']
    rot=3
    myfile=globals().get('__file__', '(noname)')
    if len(args) > 1:
        myfile=args[1]

    if len(args) < 1:
        print("usage:\tARGV=[3];exec(open('"+myfile+"').read())\t# -or-\n\t"+myfile+"blink [rotation]")

    if len(args) > 1:
        rot = int(args[1])
    if len(args) > 2:
        num = int(args[2])

    
    fonts = [glcdfont,tt14,tt24,tt32]
    
    text = 'Now is the time for all good men to come to the aid of the party.'
    
    power = Pin(m5stack.TFT_LED_PIN, Pin.OUT)
    power.value(1)
    
    spi = SPI(
        2,
        baudrate=20000000,    # was 40000000 - could be 55000000 (write) or 20000000 (read)
        miso=Pin(m5stack.TFT_MISO_PIN),
        mosi=Pin(m5stack.TFT_MOSI_PIN),
        sck=Pin(m5stack.TFT_CLK_PIN))
    
    display = ILI9341(
        spi,
        cs=Pin(m5stack.TFT_CS_PIN),
        dc=Pin(m5stack.TFT_DC_PIN),
        rst=Pin(m5stack.TFT_RST_PIN),
        w=320,
        h=240,
        r=rot)
    
    display.erase()
    display.set_pos(0,0)
    for ff in fonts:
        display.set_font(ff)
        display.print(text)

    display.fill_rectangle(0  ,0,dxm,dy,color=color565(255,0,0))
    display.fill_rectangle(dxm,0,dxm,dy,color=color565(0,255,0))

    display.fill_rectangle(dxm-5,0,10,dy,color=color565(0,0,255))
    display.fill_rectangle(0,dym-20,dx,40,color=color565(255,255,255))

    spi.deinit()

   
if 'ARGV' in locals():
    run(globals().get('__file__', '(noname)'),*ARGV)
