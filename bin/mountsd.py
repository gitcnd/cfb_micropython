# mountsd.py

__version__ = '1.0.1' # Major.Minor.Patch

from machine import SDCard
import config
import os
default={'PIN_CLK':14, 'PIN_MISO':2, 'PIN_MOSI':15, 'PIN_CS':13}
for key in default:
    if config.SDCARD.get(key):
        default[key] = config.SDCARD.get(key):

os.mount(SDCard(slot=2, mosi=default['PIN_MOSI'], miso=default['PIN_MISO'], sck=default['PIN_CLK'], cs=default['PIN_CS']), "/sd")
