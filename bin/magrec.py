# magrec.py

__version__ = '1.0.0' # Major.Minor.Patch

'''

POST magentometer data to cdc

ARGV=["2"];exec(open("bin/magrec.py").read())

'''

import time
import sys
from hmc5883l import HMC5883L
import requests
import json
from array import array

def __main__(args):
    run(args[2:])    # mipyshell first 2 arguments are "python" and "photo.py"

def run(args):
    scl=16
    sda=17
    loop=1
    ran=1

    if len(args) > 0:
        loop = int(args[0])
    if len(args) > 1:
        scl = int(args[1])
    if len(args) > 2:
        sda = int(args[2])

    print("mag loop{} scl{} sda{}".format( loop, scl, sda ))

    sensor = HMC5883L(scl=scl, sda=sda)

    while 1:
        x = [0.0] * 32#array('f', [0.0] * 32)
        y = [0.0] * 32#array('f', [0.0] * 32)
        z = [0.0] * 32#array('f', [0.0] * 32)
        for i in range(32):
            x[i], y[i], z[i] = sensor.read()
            time.sleep(0.07)    # sensor is 15hz

        #print(sensor.format_result(x, y, z))

        # Define the JSON data
        data = {'x': x, 'y': y, 'z': z}
        json_data = json.dumps(data)

        # Make the POST request
        try:
            response = requests.post('http://172.22.1.66/iot.asp', data=json_data)
            response.close()
        except:
            print("http post failed")

        time.sleep(10.0)

    #for i in range(loop):
    while 1:
        x, y, z = sensor.read()
        print(sensor.format_result(x, y, z))

        # Define the JSON data
        data = {'x': x, 'y': y, 'z': z}
        json_data = json.dumps(data)

        # Make the POST request
        response = requests.post('http://172.22.1.66/iot.asp', data=json_data)
        response.close()
        time.sleep(1.0)

    return 0


if 1: # try:
    if 'ARGV' in locals():
        run(ARGV)
    else: # can't do this - it runs before __main__ without the sh (args)
        run([])
    #    print("runS")
    #            print(sensor.format_result(x, y, z))
