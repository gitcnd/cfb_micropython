#
# The MIT License (MIT)
#
# Copyright (c) Sharil Tumin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-----------------------------------------------------------------------------

# webcam.py MVC - This is the controller C of MVC

from machine import reset
from time import sleep
import usocket as soc
import gc
#
import camera
import config as K
from wifi import Sta
from help import Setting as cam_setting
import site

gc.enable() # Enable automatic garbage collection


# set camera configuration
K.configure(camera, K.ai_thinker) # AI-Thinker PINs map - no need (default)
#camera.conf(K.XCLK_MHZ, 16) # 16Mhz xclk rate
camera.conf(K.XCLK_MHZ, 14) # 14Mhz xclk rate
#camera.conf(K.XCLK_MHZ, 13) # 14Mhz xclk rate
#camera.conf(K.XCLK_MHZ, 12) # 12Mhz xclk rate - to reduce "cam_hal: EV-EOF-OVF"

# wait for camera ready
for i in range(5):
    cam = camera.init()
    print("Camera ready?: ", cam)
    if cam: break
    else: sleep(2)
else:
    print('Timeout')
    reset() 

if cam:
   print("Camera ready")
   # wait for wifi ready


# set preffered camera setting
camera.framesize(10)     # frame size 800X600 (1.33 espect ratio)
#camera.framesize(11)     
#camera.framesize(12)    
camera.quality(5)
#camera.quality(10)
camera.brightness(3)
camera.contrast(2)       # increase contrast
#camera.contrast(0)
camera.speffect(2)       # jpeg grayscale

cam_setting['framesize']=10
cam_setting['quality']=5
cam_setting['contrast']=0
cam_setting['speffect']=2
cam_setting['brightness']=3

#site.camera=camera


buf=camera.capture()

print("Length of buf:", len(buf))

print("Contents of buf in hex:", buf.hex())

