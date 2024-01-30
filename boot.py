# boot.py

__version__ = '1.0.3' # Major.Minor.Patch

# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#os.dupterm(None, 1) # disable REPL on UART(0)

import machine, gc
global wdt
print('')    # fix terminal mode if broken by preceeding garbage
# if booting is broken, pressing GPIO0 when the boot is stuck in the loop will avoid running whatever was broken...
print("boot.py reset_cause={}".format(machine.reset_cause()))
if not machine.Pin(0,machine.Pin.IN,machine.Pin.PULL_UP).value():
    print("GPIO0 Asserted: skipping boot")
elif machine.reset_cause() == 5:
    print("soft_reset: skipping boot")
else:
    #import wdt # watchdog timer demo - caution - resets every 20s if not wdt.feed() called
    exec(open("netboot.py").read()) # runs webrepl.start()

gc.collect()
