# radar.py

__version__ = '1.0.0' # Major.Minor.Patch


from sh import human
import os
import machine
import time
import struct

def __main__(args): # ['python', '/bin/set.py', '33', '0']
    pinpwr=15   # No good - needs 5v!
    pinrx=16
    pintx=17
    baud=256000    # 1 stop, no parity

    # print(args)

    if len(args) < 2:    # never happens
        print("Usage:")
        print(args[1] + " pinrx{} pintx{} baud{}".format(pinrx, pintx, baud))
    else:
        print(args[1] + " pinrx{} pintx{} baud{}".format(pinrx, pintx, baud))
        if len(args) > 2:
            pinrx = int(args[2])
        if len(args) > 3:
            pintx = int(args[3])
        if len(args) > 4:
            baud = int(args[4])

        rpwr = machine.Pin(pinpwr, machine.Pin.OUT)
        rpwr.value(1) # Turn it on
        time.sleep(1) # give it a sec to start up

        uart = machine.UART(2, baud)            # init with given baudrate
        uart.init(baud, bits=8, parity=None, stop=1)    # init with given parameters

        # A UART object acts like a stream object and reading and writing is done using the standard stream methods:

        #   uart.read(10)    # read 10 characters, returns a bytes object
        #   uart.read()        # read all available characters
        #   uart.readline()    # read a line
        #   uart.readinto(buf)    # read and store into the given buffer
        #   uart.write('abc')    # write the 3 characters

        while True:
            bytesavail=uart.any()
            if bytesavail>0:
                got=uart.read(bytesavail)
                print(str(bytesavail) + " ",end="")

                if len(got) != struct.calcsize("I3hH3hH3hHH"):
                    print(got.encode('hex'))
                else:
                    print(struct.unpack("I3hH3hH3hHH", got))

                #print(got)
                #unpacked_data = struct.unpack('>I3hH3hH3hHH', got)
                #print(unpacked_data)



'''
uart.init(baud, bits=8, parity=None, stop=1) # init with given parameters
baudrate is the clock rate.
bits is the number of bits per character, 7, 8 or 9.
parity is the parity, None, 0 (even) or 1 (odd).
stop is the number of stop bits, 1 or 2.

tx specifies the TX pin to use.
rx specifies the RX pin to use.
rts specifies the RTS (output) pin to use for hardware receive flow control.
cts specifies the CTS (input) pin to use for hardware transmit flow control.
txbuf specifies the length in characters of the TX buffer.
rxbuf specifies the length in characters of the RX buffer.
timeout specifies the time to wait for the first character (in ms).
timeout_char specifies the time to wait between characters (in ms).
invert specifies which lines to invert.
  0 will not invert lines (idle state of both lines is logic high).
  UART.INV_TX will invert TX line (idle state of TX line now logic low).
  UART.INV_RX will invert RX line (idle state of RX line now logic low).
  UART.INV_TX | UART.INV_RX will invert both lines (idle state at logic low).
flow specifies which hardware flow control signals to use. The value is a bitmask.
  0 will ignore hardware flow control signals.
  UART.RTS will enable receive flow control by using the RTS output pin to signal if the receive FIFO has sufficient space to accept more data.
  UART.CTS will enable transmit flow control by pausing transmission when the CTS input pin signals that the receiver is running low on buffer space.
  UART.RTS | UART.CTS will enable both, for full hardware flow control.
 


Radar data output protocol

  Frame header ...  intraframe data ...  end of frame
  AA FF 03 00        (see below)        55cc

    Target 1 Information Target 2 Information Target 3 Information

Report data frame format

The specific information contained in a single target is shown in the following table

  Target X coordinate  (int 16)    signed int16 type, the highest bit 1 corresponds to positive coordinates, 0 corresponds to negative coordinates, unit mm
  target y coordinate (int 16)
  target speed (int 16)    signed int16 type, the highest bit 1 corresponds to the positive speed, 0 corresponds to the negative speed, and the other 15 bits correspond to the speed in cm/s
  distance resolution (uint 16)    uint16 type, single distance gate size, unit mm

Data example:

AA FF 03 00   0E 03 B1 86 10 00 40 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   55 CC

This set of data indicates that the radar is currently tracking a target, namely target 1 (blue field in the example). Target 2 and target 3 (corresponding to the red and black fields in the example respectively) do not exist, so their corresponding data segments are 0x00. The process of converting target 1 data into relevant information is shown below:

Target 1 x coordinate: 0x0E + 0x03 * 256 = 782

0 - 782 = -782mm

Target 1 y coordinate: 0xB1 + 0x86 * 256 = 34481

34481 - 2^15 = 1713 mm

Target 1 speed: 0x10 + 0x00 * 256 = 16

0 -16 =-16 cm/s

Target 1 distance resolution: 0x40 +0x01* 256 = 320 mm  
  
'''

