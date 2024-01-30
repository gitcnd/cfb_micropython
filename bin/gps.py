# gps.py

__version__ = '1.0.1' # Major.Minor.Patch

from machine import UART, Pin
import time
# from sh import human
import os
import machine

# AT+IPR=3686400    # change baud rate command?

def __main__(args):
    run(args[1:])    # mipyshell first 2 arguments are "python" and "blink.py"



def uart_read_ms(uart,timeout):
    start_time = time.ticks_ms()
    response = b''
    while time.ticks_diff(time.ticks_ms(), start_time) < timeout or uart.any():
        if uart.any():
            response += uart.read(uart.any())
        else:
            time.sleep_ms(50)
    return response

def append_file(fn,text):
    try:
        # Open the file in append mode ('a') and write the string
        with open(fn, 'a') as file:
            file.write(text)
        # The file is automatically closed when exiting the 'with' block

    except Exception as e:
        print("An error occurred: {e}".format(e))


def uart_write(uart,cmd):
    print("\033[92m" + repr(cmd) + "\033[0m")
    uart.write(cmd)


def getGNSS(uart,fn=None):
    uart.write('AT+CGNSSINFO\r\n')

    response = uart_read_ms(uart,2000)

    if response:    # if uart.any():
        print("got:{}".format(response))    # got:b'AT+CGNSSINFO\r\r\n+CGNSSINFO: ,,,,,,,,\r\n\r\nOK\r\n'
        if fn:
            append_file(fn,"{}\n".format(response))    # got:b'AT+CGNSSINFO\r\r\n+CGNSSINFO: ,,,,,,,,\r\n\r\nOK\r\n'

        decoded_response = response.decode()  # Decode once after reading
        lines = decoded_response.split('\r\n')

        for line in lines:
            if '+CGNSSINFO: ' in line:
                data = line.split('+CGNSSINFO: ')[1]
                parts = data.split(',')

                fix_mode = 0
                if parts[0]:
                    fix_mode = int(parts[0])

                if fix_mode in [1, 2, 3]:
                    # Parsing GNSS data
                    lat = float(parts[2])  # Latitude
                    lat_dir = parts[3]    # N/S Indicator
                    lon = float(parts[4])  # Longitude
                    lon_dir = parts[5]    # E/W Indicator

                    # Date in ddmmyy format
                    day = int(parts[6][:2])
                    month = int(parts[6][2:4])
                    year = int(parts[6][4:6])

                    # Time in hhmmss.s format
                    hour = int(parts[7][:2])
                    minute = int(parts[7][2:4])
                    second = float(parts[7][4:])

                    altitude = float(parts[8])  # MSL Altitude in meters
                    speed = float(parts[9])     # Speed over ground in knots
                    accuracy = float(parts[13]) # Position Dilution of Precision

                    print(f"Latitude: {lat} {lat_dir}, Longitude: {lon} {lon_dir}")
                    print(f"Date: {day}/{month}/{year}, Time: {hour}:{minute}:{second}")
                    print(f"Altitude: {altitude}m, Speed: {speed} knots, Accuracy: {accuracy}")
                    
                    # Check for invalid data
                    if lat == 0 or lon == 0:
                        print("Invalid GNSS Data")
                        return
                else:
                    print("No GNSS Fix")
    else:
        print("No data received from GNSS")


def run(args):
    loop=2
    dly=0.0
    fn=""
    if len(args) > 0:
        myfile = args[0]
    if len(args) > 1:
        loop = int(args[1])
    if len(args) > 2:
        dly = float(args[2])
    if len(args) > 3:
        fn = args[3]

    print("{}: loop{} delay{} outfn:{}".format(myfile, loop, dly, fn))

    # A7608 GPS modem is compatible with SIM7600 AT instructions
    # Pin configuration
    UART_BAUD      = 115200
    MODEM_TXD_PIN  = 26
    MODEM_RXD_PIN  = 27
    MODEM_PWR_PIN  = 4
    BOARD_POWER_ON = 12
    MODEM_RST_PIN  = 5

    MODEM_DTR_PIN  = 25
    BAT_ADC        = 35 
    MODEM_RI_PIN   = 33
    SD_MISO        = 2
    SD_MOSI        = 15
    SD_SCLK        = 14
    SD_CS          = 13
    TINY_GSM_RX_BUFFER = 1024


    # Initialize UART
    uart = UART(1, baudrate=UART_BAUD, tx=MODEM_TXD_PIN, rx=MODEM_RXD_PIN)    # SERIAL_8N1
    uart.init(UART_BAUD, bits=8, parity=None, stop=1)

    # Initialize control pins
    board_power = Pin(BOARD_POWER_ON, Pin.OUT)
    modem_power = Pin(MODEM_PWR_PIN, Pin.OUT)
    modem_reset = Pin(MODEM_RST_PIN, Pin.OUT)

    board_power.value(1)
    modem_power.value(1)
    time.sleep_ms(1000)

    modem_reset.value(1)
    time.sleep_ms(1000)
    modem_reset.value(0)

    print("GPS starting...")
    uart.write('AT+CGNSSPWR=1\r\n')
    response = uart_read_ms(uart,5000)
    print("GPS Ready! {}".format(response))

    while loop != 0:    # -1 for forever
        getGNSS(uart,fn)
        if dly>0.0:
            time.sleep(dly)
        loop=loop-1


if 'ARGV' in locals():
    run(globals().get('__file__', '(noname)'),*ARGV)
