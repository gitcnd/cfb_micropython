# showbmp.py

__version__ = '1.0.2' # Major.Minor.Patch

# see imgcvt.pl and alchemy -k
# ARGV=['IMG_1781_77.lcd'];exec(open('bin/showlcd.py').read())

'''


copy IMG_1781.png IMG_1781_77.png
alchemy -k IMG_1781_77.png
del IMG_1781_77.png

hexdump -C IMG_1781_77.pnm|head
00000000  50 36 0a 33 32 30 20 32  34 30 0a 32 35 35 0a ff  |P6.320 240.255..|
00000010  00 00 00 ff 00 00 00 ff  00 00 00 ff ff ff e2 dd  |................|

'''


# from sh import human # this opens the shell if not already opened
import time
import struct
import os

from ili934xnew import ILI9341, color565
from machine import Pin, SPI
import m5stack
import glcdfont
import tt14
import tt24
import tt32

dx=320
dy=240
dxm=int(dx/2)  # middle
dym=int(dy/2)


def read_bmp_header(filename):
    try:
        with open(filename, "rb") as file:
            # Read BMP header fields

            header = file.read(54)  # Read the first 54 bytes (standard BMP header size)

            # Header format for a 16-bit BMP file:
            # 2 bytes: BM (magic number)
            # 4 bytes: File size
            # 4 bytes: Reserved
            # 4 bytes: Pixel data offset
            # 4 bytes: header size 54
            # 4 bytes: Info header size (always 40 for BMP)
            # 4 bytes: Width
            # 4 bytes: Height
            # 2 bytes: Number of color planes (always 1)
            # 2 bytes: Bits per pixel (16 for 16-bit BMP)
            # 4 bytes: Compression method (usually 0 for uncompressed)
            # 4 bytes: Image size
            # 4 bytes: Horizontal pixels per meter
            # 4 bytes: Vertical pixels per meter
            # 4 bytes: Number of colors in palette
            # 4 bytes: Important colors

            header_data = struct.unpack('<2sIHHIIIIHHII4s4s4s4s', header)

            return {
                'magic_number': header_data[0].decode('ascii'),
                'file_size': header_data[1],
                'reserved': header_data[2],
                'pixel_data_offset': header_data[3],
                'header_size': header_data[4],
                'info_header_size': header_data[5],
                'width': header_data[6],
                'height': header_data[7],
                'planes': header_data[8],
                'bits_per_pixel': header_data[9],
                'compression': header_data[10],
                'image_size': header_data[11],
                'pixels_per_meter_x': header_data[12],
                'pixels_per_meter_y': header_data[13],
                'colors_in_palette': header_data[14],
            }

    except Exception as e:
        print(f"Error: {e}")
        return None

def read_bmp_headerf(file):
    try:
        # Read BMP header fields
        header = file.read(54)  # Read the first 54 bytes (standard BMP header size)
        # Header format for a 16-bit BMP file:
        # 2 bytes: BM (magic number)
        # 4 bytes: File size
        # 4 bytes: Reserved
        # 4 bytes: Pixel data offset
        # 4 bytes: header size 54
        # 4 bytes: Info header size (always 40 for BMP)
        # 4 bytes: Width
        # 4 bytes: Height
        # 2 bytes: Number of color planes (always 1)
        # 2 bytes: Bits per pixel (16 for 16-bit BMP)
        # 4 bytes: Compression method (usually 0 for uncompressed)
        # 4 bytes: Image size
        # 4 bytes: Horizontal pixels per meter
        # 4 bytes: Vertical pixels per meter
        # 4 bytes: Number of colors in palette
        # 4 bytes: Important colors

        header_data = struct.unpack('<2sIHHIIIIHHII4s4s4s4s', header)

        return {
            'magic_number': header_data[0].decode('ascii'),
            'file_size': header_data[1],
            'reserved': header_data[2],
            'pixel_data_offset': header_data[3],
            'header_size': header_data[4],
            'info_header_size': header_data[5],
            'width': header_data[6],
            'height': header_data[7],
            'planes': header_data[8],
            'bits_per_pixel': header_data[9],
            'compression': header_data[10],
            'image_size': header_data[11],
            'pixels_per_meter_x': header_data[12],
            'pixels_per_meter_y': header_data[13],
            'colors_in_palette': header_data[14],
        }

    except Exception as e:
        print(f"Error: {e}")
        return None


def __main__(args):
    run(args[2:])    # mipyshell first 2 arguments are "python" and "blink.py"

def run(args):
    while args and (args[-1] == b'' or args[-1] == ''): args.pop()

    if len(args) < 1:
        print("usage:\tARGV=['file.bmp'];exec(open('bin/showbmp.py').read())\t# -or-\n\tshowbmp file.bmp")
    else:
        bmp_filename=args[0]
        with open(bmp_filename, "rb") as bmp_file:
            header_info = {'width':320, 'height':240} #  read_bmp_headerf(bmp_file)
    
            if header_info:
                for key, value in header_info.items():
                    print(f"{key}: {value}")
    
    
            print(header_info['width'])
    
            rot=3
            # fonts = [glcdfont,tt14,tt24,tt32]
            
            text = 'Hello'
            
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
            display.set_font(tt24)
            display.print(text)
        
            display.fill_rectangle(0  ,0,dxm,dy,color=color565(255,0,0))
            display.fill_rectangle(dxm,0,dxm,dy,color=color565(0,255,0))
        
            display.fill_rectangle(dxm-5,0,10,dy,color=color565(0,0,255))
            display.fill_rectangle(0,dym-20,dx,40,color=color565(255,255,255))
    
    
            for y in range(header_info['height']):
                line=bmp_file.read(2*header_info['width'])
                display._writeblock(0, y, header_info['width']-1, y, line)
                #for x in range(header_info['width']):
                #    #px=bmp_file.read(2)
                #    display._writeblock(x, y, x, y, line[2*x:2*x+2])
                #    #display.pixel(x,y,px)
    
            spi.deinit()
    
    

if 'ARGV' in locals():
    run(ARGV)



