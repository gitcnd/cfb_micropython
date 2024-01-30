# ifup.py

__version__ = '1.0.0' # Major.Minor.Patch

if 1:
    print("Activating network")
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('yourSSID', 'your_password') # this is non-blocking

    print("Starting webrepl")
    import webrepl
    webrepl.start()

    print("Starting IDE web service on http://" + wlan.ifconfig()[0] + "/") # this never works, because non-blocking above (wlan.isconnected())
    import weditor.start
