# lightbar_espnow_server.py

__version__ = '1.0.0' # Major.Minor.Patch

# See https://docs.micropython.org/en/latest/library/espnow.html

''' Notes:-

first-encountered freq remains set

sta.config(pm=sta.PM_NONE)    # need to disable sleep, or messages get lost
if wifi is connected, need to sync select channel: print("Proxy running on channel:", sta.config("channel"))


'''

from sh import human
import os
import machine
import time
import network
import espnow

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()    # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)
offtime={} # time.time()
pduty={}
pwm={}
idle=0

while True:
    host, msg = e.recv(500)
    if msg:             # msg == None if timeout in recv()
        #print(host, msg)
        if msg == b'end':
            break

        rec=""
        pin=33
        freq=36000
        duty=0
        ontime=60

        lst = msg.split()        # split the message into a list of substrings
        if len(lst)>0:
            rec=lst[0]        # who this message is for
        if len(lst)>1:
            pin=int(lst[1])        # which light
        if len(lst)>2:
            freq=int(lst[2])    # frequency
        if len(lst)>3:
            duty=int(lst[3])    # brightness
        if len(lst)>4:
            ontime=int(lst[4])    # auto-off after this # of seconds


        if duty>65535: duty=65535
        if duty<0: duty=0
        #b'$\xdc\xc3\x9cJ`' b'esp32-d1e 33 36000 8811 2 '
        #b'esp32-d1e': set pin33 freq36000 duty8811 ontime2
        host_string = ':'.join('%02x' % b for b in host)
        print("rmt:{}\tmsg{}\ttgt:{}: set pin{} freq{} duty{} ontime{}".format(host_string, msg, rec, pin, freq, duty, ontime))

        # future - if already on and same settings - do not re-do this
        if pin in pwm:
            pwm[pin].duty_u16(duty)
        else:
            pwm[pin] = machine.PWM(pin, freq=freq, duty_u16=duty)    # create a PWM object on a pin and set freq and duty
            offtime[pin]=0
            #pwm.deinit()

        pduty[pin]=duty
        offtime[pin]=time.time()+ontime
        idle=0

        # pwm.duty_u16(32768)            # set duty to 50%
        # pwm.init(freq=5000, duty_ns=5000)    # reinitialise with a period of 200us, duty of 5us
        # pwm.duty_ns(3000)            # set pulse width to 3us
        # ESPNow.stats() (ESP32 only) Returns: (tx_pkts, tx_responses, tx_failures, rx_packets, rx_dropped_packets)

    else:            # timeout every 500ms
        if not idle:
            idle=1
            for pin in pwm:
                if pduty[pin]>0:
                    idle=0
                    if time.time()> offtime[pin]: # and pwm[pin] is not None:
                        pwm[pin].duty_u16(0)
                        pduty[pin]=0
                        #pwm[pin].deinit()
                        #pwm[pin]=None

        # e.peers_table - signal strengths... handy for testing PWM RF interference?



