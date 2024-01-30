# pins.py

__version__ = '1.0.0' # Major.Minor.Patch

from sh import human
import os
import machine
import time

def __main__(args):
    dly = 1.0
    

    if len(args) > 2:
        dly = float(args[2])
    print("pins dly{}".format(dly))

    
    # Define pins to skip (these crash the board)
    #skip_pins= [0, 2, 4, 5,              12, 13, 14, 15,     25, 26, 27,                 32, 33, 34, 35, 36, 39]
    #skip_pins= [0, 2, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 39]
    skip_pins = [            6, 7, 8, 11,                 24,             28, 29, 30, 31,                     39]
    
    # Define all other pins as inputs
    #crashes pins = [machine.Pin(i, machine.Pin.IN) for i in range(40) if i not in skip_pins]

    # Continuously read and print the pin values
    while True:
        for i in range(0,40):
            if i not in skip_pins:
                #print("Pin", i)
                #time.sleep(1)
                pin = machine.Pin(i, machine.Pin.IN) 
                #print("Pin", i, "value:", pin.value())
                print(pin.value(),end="")
                #time.sleep(1)
            else:
                print("-",end="")
        print("")
        time.sleep(dly)
