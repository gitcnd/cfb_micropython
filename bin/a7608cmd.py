# a7608cmd.py - send serial commands to an attached A7608SA-H GPS/GSM modem etc.

__version__ = '1.0.0' # Major.Minor.Patch

from machine import UART, Pin
import time
# from sh import human
import os
import machine

def __main__(args):
    run(args[2:])    # mipyshell first 2 arguments are "python" and "blink.py"


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


def run(args):
    loop=2
    if len(args) > 0:
        loop = int(args[0])

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
    uart_write(uart,'AT+CGNSSINFO\r\n')
    response = uart_read_ms(uart,5000)
    print("GPS Ready! {}".format(response))

    uart_write(uart,'AT+SIMCOMATI\r\n')
    response = uart_read_ms(uart,5000)
    print("GPS Ready! {}".format(response))


if 'ARGV' in locals():
    run(ARGV)
