# testasync.py

__version__ = '1.0.0' # Major.Minor.Patch

import asyncio
from sh import human
import os
import machine
import time

async def background_task():
    cb=0
    while True:
        # do something in the background
        print(str(cb) + " ",end="")
        cb=cb+1
        await asyncio.sleep(1)  # wait for 1 second

async def main():
    mb=0 # do something in the main program
    while True:
        print("Main program {} running...".format(mb))
        mb=mb+1
        await asyncio.sleep(2)  # wait for 2 seconds


def __main__(args): # ['python', '/bin/set.py', '33', '0']
    num = 1        # times to loop

    if len(args) < 3:
        print("Usage:")
        print(args[1] + " rot{}".format(rot))
    else:
        if len(args) > 2:
            num = int(args[2])
        if len(args) > 3:
            pin = int(args[3])

        loop = asyncio.get_event_loop()
        loop.create_task(background_task())
        loop.run_until_complete(main())
