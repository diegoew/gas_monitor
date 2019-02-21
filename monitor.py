#!/usr/bin/env python3
"""
Periodically reads gas concentration from sensors, stores the values in a local
database and uploads them to the Web service.
"""
import argparse
from datetime import datetime, timezone
import logging
import sys
import time

import openweather

from config import ADC_TYPE, DEFAULT_SECONDS_BETWEEN_READINGS, SENSOR_TYPES
import db
import adc as adc_
import uploader


adc = None

parser = argparse.ArgumentParser(
    description='Read gas sensors ' + ', '.join(SENSOR_TYPES)
    + '\nTo configure, edit file config.py.'
)

parser.add_argument('--calibrate',
                    action='store_true',
                    default=False,
                    help='Calibrate the sensors and store the results.'
                         'Do not start measuring.')


def get_ros():
    ros = []
    for i, s in enumerate(SENSOR_TYPES):
        r = db.get_ro(s)
        if r is None:
            r = calibrate(i)
        ros.append(r)
    return ros


def calibrate(i):
    r = adc.calibrate(i)
    db.store_ro(SENSOR_TYPES[i], r)
    return r


def run():
    try:
        ros = get_ros()
        delay = None
        while True:
            start = time.time()
            sys.stdout.write('\r\033[K')
            for pin_num, (sensor_type, ro) in enumerate(zip(SENSOR_TYPES, ros)):
                val = adc.read(pin_num)
                dt = datetime.now(timezone.utc).astimezone()
                logging.info('%s=%g ' % (sensor_type, val))
                temp, hum = openweather.get_temperature_and_rel_humidity()
                db.store_reading(dt, sensor_type, val, adc.RESOLUTION, ro, temp, hum)
                delay = uploader.upload(str(dt), sensor_type, val, adc.RESOLUTION, ro, temp, hum)

            try:
                delay = float(delay)
            except (TypeError, ValueError):
                delay = DEFAULT_SECONDS_BETWEEN_READINGS
            sleep = delay - time.time() + start
            if sleep > 0:
                logging.info('Wait %ss' % delay)
                time.sleep(sleep)
            elif sleep < 0:
                logging.warn('Behind by %s seconds' % abs(sleep))
    except KeyboardInterrupt:
        logging.info('Keyboard interrupt')
        db.close_connection()

if __name__ == '__main__':
    args = parser.parse_args()
    adc = adc_.create(ADC_TYPE)
    db.init()

    if args.calibrate:
        for i, _ in enumerate(SENSOR_TYPES):
            calibrate(i)
    else:
        run()
