# touchlight.py

__version__ = '1.0.0' # Major.Minor.Patch

# See https://docs.micropython.org/en/latest/library/espnow.html

''' Notes:-

sta.config(pm=sta.PM_NONE)    # need to disable sleep, or messages get lost
if wifi is connected, need to sync select channel: print("Proxy running on channel:", sta.config("channel"))

'''

from sh import human
import os
import machine
import time
import network
import espnow
import struct

pwm={}

def __main__(args): # ['python', '/bin/set.py', '33', '0']
    rec = "esp32-d1e"    # who
    pin1=33        # minibar
    pin2=26        # megabar
    pin3=32        # microbar
    pinlcd=27
    freq=36000    # hz
    ontime=2

    if len(args) > 2:
        rec = args[2]
    if len(args) > 3:
        pin1 = int(args[3])
    if len(args) > 4:
        freq = int(args[4])
    if len(args) > 5:
        ontime = int(args[5])

    print("touchlight recipient:{} pin{} freq{} ontime{}".format(rec, pin1, freq, ontime))

    i2c = machine.SoftI2C(scl=machine.Pin(32), sda=machine.Pin(33), freq=400000)
    i2c.writeto_mem(21, 0xfe, b'\xff') # tell it not to sleep
    lastx=-1
    lasty=-1
    lastg=-1


    # A WLAN interface must be active to send()/recv()
    sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
    sta.active(True)
    sta.disconnect()    # Because ESP8266 auto-connects to last Access Point

    e = espnow.ESPNow()
    e.active(True)
    #\xbb\xbb\xbb\xbb\xbb\xbb'   # MAC address of peer's wifi interface
    peer = b'\xff\xff\xff\xff\xff\xff' # broadcast mac address to all esp32's (not esp8266)
    e.add_peer(peer)      # Must add_peer() before send()

    minduty={}; maxduty={}; bufduty={}

    pino=pin1            # minibar
    minduty[pino]=6800    # anything less than this is black
    maxduty[pino]=13000    # anything more than this is full-on
    bufduty[pino]=100    # so on and off  work OK
    pino=pin2            # megabar
    minduty[pino]=9150    # anything less than this is black
    maxduty[pino]=17700    # anything more than this is full-on
    bufduty[pino]=100    # so on and off  work OK
    pino=pinlcd            # local lcd backlight
    minduty[pino]=0        # anything less than this is black
    maxduty[pino]=65535    # anything more than this is full-on
    bufduty[pino]=100    # so on and off  work OK
    pino=pin3            # microbar
    minduty[pino]=6800    # anything less than this is black
    maxduty[pino]=13000    # anything more than this is full-on
    bufduty[pino]=100    # so on and off  work OK

    mintouch=5        # screen top touch reading
    maxtouch=240        # screen bottom touch reading
    buftouch=5


    while True:
        index, gesture, x, y = struct.unpack('>BBHH',i2c.readfrom_mem(21, 0x01, 6)) # see https://docs.python.org/3/library/struct.html
        xb = x & 0xFFF
        yb = y & 0xFFF
        #data = i2c.readfrom_mem(15, 0x01, 6)
        #print(data)
        if gesture !=lastg or xb !=lastx or yb !=lasty:
            lasty=yb
            lastx=xb
            lastg=gesture
            pino=pin1
            if(yb<150): pino=pin2
            if yb>140 and yb<160: pino=pinlcd
            if(yb<70): pino=pin3

            #duty = xb * 300

            # make dim more sensitive
            #1    from    65535        74335
            #2    add    -8800        7860.909799        adj    2850
            #3    mult    7200        66474.0902
            #4    sqrt    0.4
            #5    max    260        =$H$1-(($H$5-F8)^$H$4*$H$3+$H$2)

            #duty = int(65535 - ((260-xb) ** 0.4 * 7200 - 8800))

            # 36000hz tests on 2nd smallest lightbar
            # 6900 - one LED barely lights up
            # 6920 - all very dim, one slightly brighter
            # 6950 - dimmest practical amount
            # 6980 - uniform dim
            # 7100 - noticable
            # 7200... 8000 in steps of 100: noticable
            # 8000 .. 12600 ...........200
            # 12700+ no change

            # pow    2
            # min    6800
            # max    13000
            # =F7^$B$1/(MAX(F7:F267)^$B$1)*($B$3-$B$2)+$B$2

            xbc = xb - mintouch
            if xbc < 0: xbc=0

            duty = int(xbc**2/((maxtouch-buftouch-mintouch)**2)*(maxduty[pino]-minduty[pino])+minduty[pino])

            if(duty > maxduty[pino]):
                duty=65535
            if(duty < minduty[pino]):
                duty=0


            msg=""

            if gesture:
                msg=rec + " " + str(pino) + " " + str(freq) + " " + str(duty) + " " + str(ontime) + " "
                if pino==pinlcd:    # dim our backlight
                    pass
                    if pino in pwm:
                        pwm[pino].duty_u16(duty)
                    else:
                        pwm[pino] = machine.PWM(pino, freq=freq, duty_u16=duty)    # create a PWM object on a pin and set freq and duty
                else: # remote light
                    e.send(peer, msg)    # tell other esp32 to switch the light

            print(" pin{} freq{} duty{}\tindex{} gesture{} x{}\txb{}\ty{}\tyb{}\tmsg:{}".format(pino, freq, duty, index, gesture, x, xb, y, yb, msg))

        time.sleep(0.01)

        #e.active(False)
'''

two diagonals do this:-

0 0 0 0 0 0
0 0 0 0 0 0
0 1 1 8 1 8
0 1 1 8 1 8
0 1 1 8 1 8
0 1 1 8 1 8
0 1 1 9 1 9
0 1 1 19 1 19
0 1 2 41 2 41
0 1 10 59 10 59
0 1 28 72 28 72
0 1 52 88 52 88
0 1 70 104 70 104
0 1 95 129 95 129
0 1 121 159 121 159
0 1 144 190 144 190
0 1 158 213 158 213
0 1 170 234 170 234
0 1 188 263 188 263
0 1 195 281 195 281
0 1 197 292 197 292
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 237 7 237 7
0 1 233 7 233 7
0 1 233 7 233 7
0 1 227 17 227 17
0 1 221 32 221 32
0 1 205 60 205 60
0 1 183 93 183 93
0 1 163 127 163 127
0 1 144 160 144 160
0 1 126 191 126 191
0 1 116 214 116 214
0 1 105 248 105 248
0 1 97 282 97 282
0 1 92 295 92 295
0 1 95 297 95 297
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0


'''
