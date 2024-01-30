# lightbar_ctrl.py

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


def __main__(args): # ['python', '/bin/set.py', '33', '0']
    rec = ""    # who
    pin=33
    freq=36000    # hz
    duty=32768    # 0 to 65535
    ontime=60

    if len(args) > 2:
        rec = args[2]
    if len(args) > 3:
        pin = int(args[3])
    if len(args) > 4:
        freq = int(args[4])
    if len(args) > 5:
        duty = int(args[5])
    if len(args) > 6:
        ontime = int(args[6])
     

    print("lightbar_ctrl rec:{} pin{} freq{} duty{} ontime{}".format(rec, pin, freq, duty, ontime))
     
    if rec:

        # A WLAN interface must be active to send()/recv()
        sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
        sta.active(True)
        sta.disconnect()    # Because ESP8266 auto-connects to last Access Point

        e = espnow.ESPNow()
        e.active(True)
        #\xbb\xbb\xbb\xbb\xbb\xbb'   # MAC address of peer's wifi interface
        peer = b'\xff\xff\xff\xff\xff\xff' # broadcast mac address to all esp32's (not esp8266)
        e.add_peer(peer)      # Must add_peer() before send()


        e.send(peer, rec + " " + str(pin) + " " + str(freq) + " " + str(duty) + " " + str(ontime) + " ")    # tell other esp32 to switch the light

        e.active(False)

