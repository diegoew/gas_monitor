import Adafruit_ADS1x15
from config import ADS1115_GAIN

adc = None


def init():
    global adc
    adc = Adafruit_ADS1x15.ADS1115()


def read(pin_num):
    return adc.read_adc(pin_num, gain=ADS1115_GAIN)


def calibrate(pin_num):
    return None
