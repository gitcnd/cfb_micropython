# config.py - put all your MCU and Environemnt-specific configuration in here (NOT passwords)

# This file defines a Singleton class, _Config, which provides a single point of access to
# configuration settings throughout the application. Being a Singleton ensures that only one
# instance of this class exists during the runtime of the application. This design pattern
# is useful for managing resources that are global in nature (like configuration settings) in a
# controlled manner.

from micropython import const

__version__ = '1.0.0'

class _Config:
    _instance = None

    @staticmethod
    def getInstance(): # Static access method.
        if _Config._instance is None:
            _Config()
        return _Config._instance

    def __init__(self):
        # Constructor is private to prevent multiple instantiations.
        if _Config._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            _Config._instance = self
            self.__version__=__version__

            # Get WiFi and Passwords first:-
            try:
                # Create the file .credentials.py, and put inside it the variables WIFI_SSID and WIFI_PASSWORD
                from _credentials import WIFI_CREDENTIALS,HOSTNAME
            except ImportError:
                WIFI_CREDENTIALS = []; HOSTNAME='GuPyDevice'
                print('CAUTION: _credentials.py WiFi and HostName settings file not found!')

            self.HOSTNAME = HOSTNAME  # to access your project via http://GuPyDevice.local
            self.WIFI_CREDENTIALS = WIFI_CREDENTIALS

            self.GPRS_APN='iot.1nce.net'  # Mobile SIM General Packet Radio Service - Access Point Name
            self.GPRS_USER=''
            self.GPRS_PASS=''

            self.GPRS_UART_BAUD= const(115200)
            self.GPRS_PIN_DTR  = const(25)
            self.GPRS_PIN_TX   = const(26)
            self.GPRS_PIN_RX   = const(27)
            self.GPRS_PWR_PIN  = const(4)
            self.GPRS_BAT_ADC  = const(35)
            self.GPRS_BAT_EN   = const(12)
            self.GPRS_PIN_RI   = const(33)
            self.GPRS_RESET    = const(5)

            self.LOGHOST='216.218.163.124'
            self.LOGPATH='/.well-known/iot.asp/TinyGSM/v' + __version__ + '/'
            self.LOGPROTOCOL='http'
            self.LOGPORT=const(80)

            self.LED_BUILTIN = const(33)  # Example GPIO pin number for onboard LED
            self.LED_STATEON = const(0)   # Write this to turn the LED on
            self.LED_STATEOFF = const(1)  # Write this to turn the LED off
            self.PIN_FLASHLIGHT = const(4)  # Example GPIO pin number for onboard LED
            self.FLASHLIGHT_STATEON = const(1)  # Write this to turn the CREE flashlight on
            self.FLASHLIGHT_STATEOFF = const(0)  # Write this to turn the CREE flashlight off
            self.PSRAM = { 'PIN_CLK':const(6), 'PIN_SD0':const(7), 'PIN_SD1':const(8), 'PIN_SD2':const(9), 'PIN_SD3':const(10), 'PIN_CMD':const(11) }
            if 'iLilyGo' in HOSTNAME:
                self.SDCARD = { 'PIN_CLK':const(14), 'PIN_CMD':const(-1), 'PIN_DATA0':const(-1), 'PIN_DATA1':const(-1), 'PIN_DATA2':const(-1), 'PIN_DATA3':const(-1), 'PIN_MISO':const(2), 'PIN_MOSI':const(15), 'PIN_CS':const(13) } # LilyGo T-A7608
            else:
                self.SDCARD = { 'PIN_CLK':const(14), 'PIN_CMD':const(15), 'PIN_DATA0':const(2), 'PIN_DATA1':const(4), 'PIN_DATA2':const(12), 'PIN_DATA3':const(13) } # esp32 cam # config.SDCARD.get('PIN_CLK'):

            self.NORM, self.RED, self.GRN, self.YEL, self.NAV, self.BLU, self.SAVE, self.REST, self.CLR, self.WHT = "\033[0m", "\033[31;1m", "\033[32;1m", "\033[33;1m", "\033[34;1m", "\033[36;1m", "\033[s", "\033[u", "\033[K", "\033[1m"
            #uncomment this line to disable ANSI colors:  self.NORM, self.RED, self.GRN, self.YEL, self.NAV, self.BLU, self.SAVE, self.REST, self.CLR = "", "", "", "", "", "", "", "", ""


            # Camera configuration for the actual camera you are using on your board, and how it is wired up:
            # (comment-out the ai_thinker and un-comment yours)
            self.CAMERA = [ # This is camera[0]
                { # AI-Thinker esp32-cam board's OV2640
                  'NAME': 'ai_thinker', 'PIN_PWDN': const(32), 'PIN_RESET': const(-1), 'PIN_XCLK': const(0), 'PIN_SIOD': const(26), 'PIN_SIOC': const(27), 'JPEG_QUALITY': const(10),
                  'PIN_D0': const(5), 'PIN_D1': const(18), 'PIN_D2': const(19), 'PIN_D3': const(21), 'PIN_D4': const(36), 'PIN_D5': const(39), 'PIN_D6': const(34), 'PIN_D7': const(35),
                  'PIN_VSYNC': const(25), 'PIN_HREF': const(23), 'PIN_PCLK': const(22), 'XCLK_MHZ': const(16), 'PIXFORMAT': const(5), 'FRAMESIZE': const(10), 'PIN_PWDN': const(32), 'FB_COUNT': const(1) 
                },
                # If you have more than 1 camera attached to your board at the same time, those additional camera configurations can be added here as new list items.

                #{ # New 2022 esp32vrover dev
                #  'NAME': 'esp_eye', 'PIN_RESET': const(-1), 'PIN_XCLK': const(4), 'PIN_SIOD': const(18), 'PIN_SIOC': const(23), 'JPEG_QUALITY': const(10), 
                #  'PIN_D0': const(34), 'PIN_D1': const(13), 'PIN_D2': const(14), 'PIN_D3': const(35), 'PIN_D4': const(39), 'PIN_D5': const(38), 'PIN_D6': const(37), 'PIN_D7': const(36),
                #  'PIN_VSYNC': const(5), 'PIN_HREF': const(27), 'PIN_PCLK': const(25), 'XCLK_MHZ': const(16), 'PIXFORMAT': const(5), 'FRAMESIZE': const(10), 'PIN_PWDN': const(-1), 'FB_COUNT': const(1),
                #},

                #{ # esp32 wrover dev 
                #  'NAME': 'wrover_dev', 'PIN_RESET': const(-1), 'PIN_XCLK': const(21), 'PIN_SIOD': const(26), 'PIN_SIOC': const(27), 'JPEG_QUALITY': const(10), 
                #  'PIN_D0': const(4), 'PIN_D1': const(5), 'PIN_D2': const(18), 'PIN_D3': const(19), 'PIN_D4': const(36), 'PIN_D5': const(39), 'PIN_D6': const(34), 'PIN_D7': const(35),
                #  'PIN_VSYNC': const(25), 'PIN_HREF': const(23), 'PIN_PCLK': const(22), 'XCLK_MHZ': const(12), 'PIXFORMAT': const(5), 'FRAMESIZE': const(10), 'PIN_PWDN': const(32), 'FB_COUNT': const(1),
                #},

                #{ # Red Board (has internal clock for camera set at 12Mhz)
                #  'NAME': 'red_board', 'PIN_RESET': const(-1), 'PIN_XCLK': const(-1,), 'PIN_SIOD': const(26), 'PIN_SIOC': const(27), 'JPEG_QUALITY': const(10), 
                #  'PIN_D0': const(5, ) 'PIN_D1': const(18,) 'PIN_D2': const(19,) 'PIN_D3': const(21,) 'PIN_D4': const(36), 'PIN_D5': const(39), 'PIN_D6': const(34), 'PIN_D7': const(35),
                #  'PIN_VSYNC': const(25), 'PIN_HREF': const(23), 'PIN_PCLK': const(22), 'XCLK_MHZ': const(12,), 'PIXFORMAT': const(5), 'FRAMESIZE': const(10), 'PIN_PWDN': const(32), 'FB_COUNT': const(1),
                #},

                #{ # XIAO ESP32S3 Sense Camera
                #  'NAME': 'xiao_s3_sense', 'PIN_RESET': const(-1), 'PIN_XCLK': const(10,) 'PIN_SIOD': const(40), 'PIN_SIOC': const(39), 'JPEG_QUALITY': const(12), 
                #  'PIN_D0': const(15), 'PIN_D1': const(17), 'PIN_D2': const(18), 'PIN_D3': const(16), 'PIN_D4': const(14), 'PIN_D5': const(12), 'PIN_D6': const(11), 'PIN_D7': const(48),
                #  'PIN_VSYNC': const(38), 'PIN_HREF': const(47), 'PIN_PCLK': const(13), 'XCLK_MHZ': const(14,) 'PIXFORMAT': const(5), 'FRAMESIZE': const(10), 'PIN_PWDN': const(-1,) 'FB_COUNT': const(1),
                #},

                #{ # LILYGO T-Camera esp32s3 V1.6
                #  'NAME': 'lilygo_t_camera', 'PIN_RESET': const(39), 'PIN_XCLK': const(38,) 'PIN_SIOD': const(5), 'PIN_SIOC': const(4), 'JPEG_QUALITY': const(12), 
                #  'PIN_D0': const(14), 'PIN_D1': const(47), 'PIN_D2': const(48), 'PIN_D3': const(21), 'PIN_D4': const(13), 'PIN_D5': const(11), 'PIN_D6': const(10), 'PIN_D7': const(9),
                #  'PIN_VSYNC': const(8), 'PIN_HREF': const(18), 'PIN_PCLK': const(12), 'XCLK_MHZ': const(14), 'PIXFORMAT': const(5), 'FRAMESIZE': const(10), 'PIN_PWDN': const(-1,) 'FB_COUNT': const(2),
                #},

                #{ # FREENOVE esp32s3 WROOM FNK0085 A1B0
                #  'NAME': 'freenove_fnk0085', 'PIN_RESET': const(-1), 'PIN_XCLK': const(15,) 'PIN_SIOD': const(4), 'PIN_SIOC': const(5), 'JPEG_QUALITY': const(12), 
                #  'PIN_D0': const(11), 'PIN_D1': const(9), 'PIN_D2': const(8), 'PIN_D3': const(10), 'PIN_D4': const(12), 'PIN_D5': const(18), 'PIN_D6': const(17), 'PIN_D7': const(16),
                #  'PIN_VSYNC': const(6), 'PIN_HREF': const(7), 'PIN_PCLK': const(13), 'XCLK_MHZ': const(14), 'PIXFORMAT': const(5), 'FRAMESIZE': const(10), 'PIN_PWDN': const(-1,) 'FB_COUNT': const(2),
                #},

                #{ # Test 
                #  'NAME': 'wrover_test', 'PIN_RESET': const(-1), 'PIN_XCLK': const(21), 'PIN_SIOD': const(26), 'PIN_SIOC': const(27), 'JPEG_QUALITY': const(10), 
                #  'PIN_D0': const(4), 'PIN_D1': const(5), 'PIN_D2': const(18), 'PIN_D3': const(19), 'PIN_D4': const(36), 'PIN_D5': const(39), 'PIN_D6': const(34), 'PIN_D7': const(35),
                #  'PIN_VSYNC': const(25), 'PIN_HREF': const(23), 'PIN_PCLK': const(22), 'XCLK_MHZ': const(12), 'PIXFORMAT': const(5), 'FRAMESIZE': const(10), 'PIN_PWDN': const(-1), 'FB_COUNT': const(1),
                #},

            ] # self.CAMERA

# Module level attribute access methods
def __getattr__(name):
    return getattr(_Config.getInstance(), name)

def __setattr__(name, value):
    return setattr(_Config.getInstance(), name, value)

# Usage example
#import config
#print(config.HOSTNAME)
#print(config.LED_BUILTIN)
