import logging

import spidev

from config import SENSOR_TYPES, LOAD_RESISTANCES, AIR_RESISTANCE_RATIOS


spi = None


def init():
    global spi
    spi = spidev.SpiDev()


def read(pin_num):
    """
    :return SPI data from the MCP3008 analogue-to-digital converter (ADC),
    from 8 channels in total.
    """
    assert 0 <= pin_num < len(SENSOR_TYPES), 'Invalid pin number: %s' % pin_num
    r = spi.xfer2([1, 8 + pin_num << 4, 0])
    return ((r[1] & 3) << 8) + r[2]


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
    print('Calibrate ' + sensor_type)
    logging.info('Calibrate ' + sensor_type)

    val = 0.0
    for _ in range(50):
        val += read(pin_num)
    val /= 50

    if val == 0:
        val += 0.0000001

    lr = LOAD_RESISTANCES[pin_num]
    arr = AIR_RESISTANCE_RATIOS[pin_num]
    ro = (1023 / val - 1) * lr / arr

    print('Val:', val, 'Ro:', ro)
    logging.info('Ro=%g', ro)

    return ro
