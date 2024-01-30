# netboot.py

__version__ = '1.0.1' # Major.Minor.Patch

# This file is executed on every boot (including wake-boot from deepsleep) through boot.py
#import esp
#esp.osdebug(None)
import os
import platform
import config
import _thread
import time
import gc

def __main__(args):
    num = 10
    if len(args) > 2:
        num = int(args[2])
        print("arg")
    print("main")


def check_connection(wlan):
    while not wlan.isconnected():
        time.sleep(1)  # Check every second
    host = wlan.config('dhcp_hostname')
    print('\nWifi connected as {}http://{}.local/{} {} {}net={} gw={} dns={}\n'.format(config.GRN, host, config.YEL, wlan.ifconfig()[0], config.NORM, *wlan.ifconfig()[1:]))
    #print("Connected. IP Address:", config.GRN, wlan.ifconfig()[0], config.NORM)

def staup(noweb=None):
    import network
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    ap_if.config(essid=config.HOSTNAME, password=config.WIFI_CREDENTIALS[0][-1], authmode=network.AUTH_WPA2_PSK) # Use same password as their first access-point listed in their config
    print('\nAUTH_WPA2_PSK Access point named {}{}{} up. ip={} net={} gw={} dns={}\n'.format(config.BLU,config.HOSTNAME, config.NORM, *ap_if.ifconfig()[0:]))

def ifup(noweb=None):
    print(platform.platform() + " built on " + platform.python_compiler())
    print("Activating network")
    import network
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():

        wlan.active(True)
        #mac = wlan.config('mac')
        #host = 'esp32-' + ''.join('{:02x}'.format(b) for b in mac[3:])
        wlan.config(dhcp_hostname = config.HOSTNAME)    # sets mDNS hostname, e.g. mpy-esp32-lcd02.local
        wlan.connect(*config.WIFI_CREDENTIALS[0]) # this is non-blocking

        # Start a new thread to check the connection status
        _thread.start_new_thread(check_connection, (wlan,))
    else:
        print("Network up already. IP Address:", config.GRN, wlan.ifconfig()[0], config.NORM)

    if not noweb:
        print("Starting webrepl on http://"+config.HOSTNAME+".local / http://" + wlan.ifconfig()[0] + "/")
        import webrepl
        webrepl.start()

        print("Starting IDE web service is on http://"+config.HOSTNAME+".local / http://" + wlan.ifconfig()[0] + "/") # this never works, because non-blocking above (wlan.isconnected())
        import weditor.start


ARGV=[4,3,0.1,0.1];exec(open('bin/blink.py').read());gc.collect()# strobe the flash on ESP32CAM so we can see it booted

if ( 'if.up' in os.listdir() ):
    ifup()
else:
    print(config.GRN+"http://"+config.HOSTNAME+".local"+config.NORM+config.WHT,"- Type ifup() to start net and web,",config.NORM,"or ifup(1) for net only.  touch /if.up to auto-start at boot")

if ( 'sta.up' in os.listdir() ):
    staup()

# Example usage
# ifup()


# auto-run if such a file exists
try:
    gc.collect()
    fne=''
    for fn in ['autoexec.py', 'autoexec2.py']:
        fne=fn
        ARGV=['boot']
        exec(open(fn).read())
        gc.collect()
except Exception as e:
    print(f"Not running {fn} Error: {e}")
    pass

gc.collect()
