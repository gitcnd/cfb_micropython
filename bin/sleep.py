# sleep.py

__version__ = '1.0.0' # Major.Minor.Patch

from sh import human
import os
import time
import network, machine, espnow


def wifi_reset(): # Reset wifi to AP_IF off, STA_IF on and disconnected
    sta = network.WLAN(network.STA_IF); sta.active(False)
    ap = network.WLAN(network.AP_IF); ap.active(False)
    sta.active(True)
    while not sta.active():
        time.sleep(0.1)
    sta.disconnect() # For ESP8266
    while sta.isconnected():
        time.sleep(0.1)
    return sta, ap


def __main__(args):
    secs = 10
    loops = 5
    if len(args) > 2:
        secs = int(args[2])
    if len(args) > 3:
        loops = int(args[3])

    print("sleep secs{} loops{}".format(secs,loops))

    sta, ap = wifi_reset() # Reset wifi to AP off, STA on and disconnected
    sta.config(channel=6)
    peer = b'0\xaa\xaa\xaa\xaa\xaa' # MAC address of peer
    e = espnow.ESPNow()
    e.active(True)
    try:
        e.add_peer(peer) # Register peer on STA_IF
    except Exception as err:
        print("peer already connected? e={}".format(err))
    while loops>0:
        print('Sending ping...')
        if not e.send(peer, b'ping'):
            print('Ping failed!')
        sta.active(False) # Disable the wifi before sleep
        print('Going to sleep...')
        machine.lightsleep(1000 * secs) # Sleep for X seconds
        sta.active(True)
        sta.config(channel=6) # Wifi loses config after lightsleep()
        loops=loops-1
