# blink.py

__version__ = '1.0.3' # Major.Minor.Patch

# from sh import human # this opens the shell if not already opened
import machine
import time


def __main__(args):
    run(args[1:])    # mipyshell first 2 arguments are "python" and "blink.py"

def run(*args):
    print(args)
    args = list(args)
    while args and (args[-1] == b'' or args[-1] == ''): args.pop()  # strip empty endings
    num = 3
    pin = 4
    tion = 1.0
    toff = 1.0
    print(args)

    # if args and args[-1] == "&": args.pop()

    if len(args) < 2:
        print("usage:\tARGV=[4,3,0.3,0.3];exec(open('bin/blink.py').read())\t# -or-\n\tblink 4 3 0.3 0.3")

    if len(args) > 1:
        pin = int(args[1])
    if len(args) > 2:
        num = int(args[2])
    if len(args) > 3:
        tion = float(args[3])
    if len(args) > 4:
        toff = float(args[4])

    if not num:
        num = 10

    print("blink pin{} loop{} ondelay{} offdelay{}".format(pin, num, tion, toff))
    led = machine.Pin(pin, machine.Pin.OUT)

    while num>0:
        led.value(1)
        time.sleep(tion)
        led.value(0)
        time.sleep(toff)
        num=num-1

if 'ARGV' in locals():
    run(globals().get('__file__', '(noname)'),*ARGV)
