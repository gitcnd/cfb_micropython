# mag.py

__version__ = '1.0.0' # Major.Minor.Patch

''' Can be run 

    ARGV=["2"];exec(open("bin/mag.py").read())
  or

    import sh
    mag 2
'''

import time
import sys
from hmc5883l import HMC5883L
global ran
ran=0

def __main__(args):
    global ran
    print("main")
    print(args)
    if ran==0:
        run(args[2:])    # mipyshell first 2 arguments are "python" and "photo.py"

def run(args):
    global ran
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

    for i in range(loop):
        x, y, z = sensor.read()
        print(sensor.format_result(x, y, z))
        time.sleep(1.0)

    return 0


if 1: # try:
    global ran
    if 'ARGV' in locals():
        print("run")
        run(ARGV)
    #can't do this - it runs before __main__ without the sh (args)
    #else:
    #    print("runS")
    #    # print(sys.argv)
    #    run(sys.argv[1:])    # linux python 1st arg is filename
#except Exception as e:
#    # print(e) # name 'ARGV' isn't defined
#    ping([])

