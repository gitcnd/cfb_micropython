# ifconfig.py

__version__ = '1.0.0' # Major.Minor.Patch

import network


def __main__(args):
    w = network.WLAN(network.STA_IF)
    ic = w.ifconfig()
    print ("WiFi: inet {} netmask {} broadcast {}".format(ic[0], ic[1], ic[2]))
    print ("\t  status: {}".format("Active" if w.isconnected() else "Inactive"))
    print ("\t  DNS {}".format(ic[3]))


