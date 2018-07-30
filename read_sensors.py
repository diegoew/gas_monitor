#!/usr/bin/env python
"""
Script to periodically read gas concentration measurements from sensors and
optionally upload them to a Web service.
"""
import argparse
from datetime import datetime, timezone
import logging
import sys
import time

import requests
import spidev

from config import REPEAT_DELAY_SECONDS, SERVER_URL, DEVICE_ID, LAT, LON, \
    SENSOR_TYPES, LOAD_RESISTANCES, AIR_RESISTANCE_RATIOS


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

parser = argparse.ArgumentParser(
    description='Read gas sensors ' + ', '.join(SENSOR_TYPES)
    + '\nTo configure, edit file config.py.'
)
spi = spidev.SpiDev()


def read_adc(pin_num):
    """
    :return SPI data from the MCP3008 analogue-to-digital converter (ADC),
    from 8 channels in total.
    """
    if not 0 <= pin_num <= 7:
        return -1
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
        val += read_adc(pin_num)
    val /= 50

    if val == 0:
        val += 0.0000001

    lr = LOAD_RESISTANCES[pin_num]
    arr = AIR_RESISTANCE_RATIOS[pin_num]
    ro = (1023 / val - 1) * lr / arr

    print('Val:', val, 'Ro:', ro)
    logging.info('Ro=%g' % ro)

    return ro


def timestamp():
    td_str = datetime.now(timezone.utc).astimezone().strftime(DATETIME_FORMAT)
    return td_str[:-2] + ':' + td_str[-2:]


def upload(sensor_type, reading, ro=None):
    data = dict(
        deviceId=DEVICE_ID,
        instant=timestamp(),
        latitude=LAT,
        longitude=LON,
        sensorType=sensor_type,
        reading=reading,
    )
    if ro is not None:
        data['ro'] = ro
    response = requests.post(SERVER_URL, data=data)
    response.raise_for_status()


def run():
    spi.open(0, 0)

    try:
        print('Press Ctrl+C to abort')
        logging.info('Program started')

        ros = [calibrate(i) for i in range(len(SENSOR_TYPES))]

        print('\nRead sensors every %s seconds...' % REPEAT_DELAY_SECONDS)
        while True:
            sys.stdout.write('\r\033[K')
            for pin_num, (sensor_type, ro) in enumerate(zip(SENSOR_TYPES, ros)):
                val = read_adc(pin_num)
                sys.stdout.write('%s:%g ' % (sensor_type, val))
                sys.stdout.flush()
                upload(sensor_type, val, ro)
                time.sleep(REPEAT_DELAY_SECONDS)

    except KeyboardInterrupt:
        print('\nAbort by user')
        logging.info('Abort by user')


if __name__ == '__main__':
    args = parser.parse_args()
    run()
