# cameratest.py

__version__ = '1.0.0' # Major.Minor.Patch

# See https://lemariva.com/blog/2020/06/micropython-support-cameras-m5camera-esp32-cam-etc

from sh import human
import os
import machine
import time
import camera

def __main__(args): # ['python', '/bin/set.py', '33', '0']


    if len(args) < 0:
        print("set pin{} value{}".format(pin, num))
    else:
        #if len(args) > 2: pin = int(args[2])


        # ESP32-CAM (default configuration) - https://bit.ly/2Ndn8tN
        camera.init(0, format=camera.JPEG)  

        # M5Camera (Version B) - https://bit.ly/317Xb74
        camera.init(0, d0=32, d1=35, d2=34, d3=5, d4=39, d5=18, d6=36, d7=19, format=camera.JPEG, xclk_freq=camera.XCLK_10MHz, href=26, vsync=25, reset=15, sioc=23, siod=22, xclk=27, pclk=21)

        # These parameters: format=camera.JPEG, xclk_freq=camera.XCLK_10MHz are standard for both cameras.
        # You can try using a faster xclk (20MHz), this also worked with the esp32-cam and m5camera 
        # but the image was pixelated and somehow green.

        buf = camera.capture()

