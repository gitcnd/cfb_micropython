# wifi.py

__version__ = '1.0.1' # Major.Minor.Patch

import network

def __main__(args):
    if len(args) == 2:
        print ("Usage:")
        print ("wifi status - prints wifi client status")
        print ("wifi on - activate wifi client")
        print ("wifi off - deactivate wifi client")
        print ("wifi scan - list visible networks")
        print ("wifi connect <SSID> <PSK> - connect to network")
        print ("wifi ap - prints Access Point status")
        print ("wifi ap on - activate Access Point")
        print ("wifi ap off - deactivate Access Point")
        return


    authmodes = {
        network.AUTH_OPEN: "Open    ",
        network.AUTH_WEP: "WEP     ",
        network.AUTH_WPA_PSK: "WPA-PSK ",
        network.AUTH_WPA2_PSK: "WPA2-PSK",
        network.AUTH_WPA_WPA2_PSK: "WPA/WPA2-PSK"
        # network.AUTH_WPA2_ENTERPRISE: "WPA2-Enterprise"
    }

    sta_if = network.WLAN(network.STA_IF)
    cmd = args[2]
    if cmd == "on":
        sta_if.active(True)
    elif cmd == "off":
        sta_if.active(False)
    elif cmd == "status":
        print ("WiFi is {}".format("Active" if sta_if.active() == True else "Inactive"))
        print ("Status {}".format(sta_if.status()))
        if sta_if.isconnected():
            print ("WiFi connection is {}".format("Established" if sta_if.isconnected() else "Not connected"))
    elif cmd == "scan":
        print ("Hid Ch\tSig(%)\t\tauth    \tBSSID            \tSSID")
        #  (b'Office TV.v,', b'\xfa\x8f\xcaW\xef$', 6, -54, 0, False)
        for (ssid, bssid, channel, RSSI, authmode, hidden) in sta_if.scan():
            mac_string = ':'.join('%02x' % b for b in bssid)
            print ("{} {}\t{}({}%)\t{}\t{}\t{}".format("Yes" if hidden else "No ", channel, RSSI, int(0.5+(95+RSSI)*(100/65)), authmodes.get(authmode, "Unknown") , mac_string, ssid  ))
    elif cmd == "connect":
        print ("Connecting to {}".format(args[3]))
        sta_if.connect(args[3], args[4])
        while not sta_if.isconnected():
            pass
        print ("Connected")
    elif cmd == "ap":
        ap_if = network.WLAN(network.AP_IF)
        cmd = args[3]
        if cmd == "on":
            ap_if.active(True)
        elif cmd == "off":
            ap_if.active(False)
        else:
            print ("Access point is {}".format("Active" if ap_if.active() == True else "Inactive"))

