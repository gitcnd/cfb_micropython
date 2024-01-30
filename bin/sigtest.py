# sigtest.py

__version__ = '1.0.0' # Major.Minor.Patch

# See if backlight pwm interferes with wifi...

from sh import human
import os
import machine
import time
import network

def __main__(args): # ['python', '/bin/set.py', '33', '0']
    pin = 27    # backlight
    freq=1000    # hz
    duty=32768    # 0 to 65535
    ton=1.0
    toff=1.0
    voff=0        # what "off" means (inverted for some LEDs)

    # print(args)


    sta_if = network.WLAN(network.STA_IF)
    pwm = machine.PWM(pin, freq=freq, duty_u16=duty)    # create a PWM object on a pin and set freq and duty
    print ("freq\tduty\tChannel\tSignal%\tdBm\tMAC?             \tSSID")
    for freq in [50, 100, 200, 300, 400, 500, 750, 1000, 1250, 1500, 2000, 2500, 3000, 3500, 4500, 5500, 7000, 8192, 10000, 12500, 15000, 20000, 25000, 30000, 35000]:
        pwm.init(freq=freq)
        for duty in [16384, 21841, 32767]:
            pwm.duty_u16(duty)
            for redo in [1,2,3]:
                for net in sta_if.scan():
                    mac_string = ':'.join('%02x' % b for b in net[1])
                    print ("{}\t{}\t{}\t{}%\t{}\t{}\t{}\t{}".format(freq,duty,net[2], int(0.5+(95+net[3])*(100/65)), net[3], mac_string, net[0],redo ))

    pwm.deinit()
