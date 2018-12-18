"""
This is an 8-channel, 16-bit analog-to-digital converter. It supports negative
values, but sensors only supply positive values. So the resolution for those
is 16 - 1 bits, or 2^15 - 1 = 32767 values.
"""
import logging

import Adafruit_ADS1x15

from config import ADS1115_GAIN, SENSOR_TYPES, LOAD_RESISTANCES,\
    AIR_RESISTANCE_RATIOS


RESOLUTION = 32767

adc = None


def init():
    global adc
    adc = Adafruit_ADS1x15.ADS1115()


def read(pin_num):
    return adc.read_adc(pin_num, gain=ADS1115_GAIN)


def calibrate(pin_num):
    """Calibrate sensor.
    :return Ro, the calculated sensor resistance for the given sensor type

    Ro as the sensor resistance at a specific calibration gas. It was defined by
    sensor manufacturer (see the data sheet linked from the README document).
    But because we do not have pure gases available, we approximate Ro using Rs,
    the resistance at various concentrations of gases, and the ratio Rs/Ro which
    is almost constant for pure air and is given by the manufacturer.
    """
    sensor_type = SENSOR_TYPES[pin_num]
    logging.info('Calibrate ' + sensor_type)
    val = 0.0
    for _ in range(50):
        val += read(pin_num)
    val /= 50
    if val == 0:
        val += 0.0000001

    lr = LOAD_RESISTANCES[pin_num]
    arr = AIR_RESISTANCE_RATIOS[pin_num]
    ro = (32767 / val - 1) * lr / arr

    logging.info('Ro=%g', ro)

    return ro
