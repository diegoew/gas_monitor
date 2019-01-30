#!/usr/bin/env python3
"""
Script to periodically read gas concentration measurements from sensors,
record them to a local database and upload them to a Web service.
"""
import argparse
from datetime import datetime, timezone
import logging
import re
import sys
import time

import requests
import openweather

from config import REPEAT_DELAY_SECONDS, SERVER_URL, DEVICE_ID, LAT, LON, \
    SENSOR_TYPES, ADC_TYPE
import db
import adc as adc_


SENSOR_INTERVAL_STR = 'secondsBetweenReadings'

dt_format = r'(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})' \
            r' (?P<time>[0-9]{2}:[0-9]{2}:[0-9]{2})' \
            r'.[0-9]{6}' \
            r'(?P<tz>-[0-9]{2}:[0-9]{2})'
dt_re = re.compile(dt_format)

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


def timestamp(dt):
    """Assume a timestring with format yyyy-mm-dd HH:MM:SS.uuuuuu-hh:mm.
    Return a timestring with format yyyy-mm-ddTHH:MM:SS-hh:mm
    Example:
        input:  2018-12-18 22:23:35.901293-08:00
        output: 2018-12-18T22:23:35-08:00
        """
    m = dt_re.match(dt)
    return m.group('date') + 'T' + m.group('time') + m.group('tz')


def upload(dt, sensor_type, reading, ro=None, temperature=None,
           rel_humidity=None):
    data = dict(
        deviceId=DEVICE_ID,
        instant=timestamp(dt),
        latitude=LAT,
        longitude=LON,
        sensorType=sensor_type,
        reading=reading,
        resolution=adc.RESOLUTION,
    )
    if ro is not None:
        data['ro'] = ro
    if temperature is not None:
        data['tempInCelsius'] = temperature
    if rel_humidity is not None:
        data['relativeHumidity'] = rel_humidity
    response = requests.post(SERVER_URL, data=data)
    response.raise_for_status()
    return response.json()


def upload_recorded():
        not_uploaded = db.get_not_uploaded()
        # Upload each measurement and record its upload timestamp
        for id_, dt, sensor_type, reading, ro, temperature, rel_humidity, _ \
                in not_uploaded:
            try:
                result = upload(dt, sensor_type, reading, ro, temperature, rel_humidity)
            except Exception as e:
                logging.error('Failed to upload measurement %s: %s', id_, e)
                break

            try:
                db.record_uploaded_time(id_)
            except Exception as e:
                logging.error('Failed to record the upload timestamp for'
                              ' measurement %s: %s', id_, e)
                break

            return result


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
    db.init()

    try:
        logging.info('\nPress Ctrl+C to stop')

        ros = get_ros()

        logging.info('\nRead sensors every %s seconds...' % REPEAT_DELAY_SECONDS)
        while True:
            start = time.time()

            sys.stdout.write('\r\033[K')
            for pin_num, (sensor_type, ro) in enumerate(zip(SENSOR_TYPES, ros)):
                val = adc.read(pin_num)
                dt = datetime.now(timezone.utc).astimezone()
                sys.stdout.write('%s=%g ' % (sensor_type, val))
                sys.stdout.flush()
                temp, hum = openweather.get_temperature_and_rel_humidity()
                db.store_measurement(dt, sensor_type, val, ro, temp, hum)
                response = upload_recorded()
                delay = response.get(SENSOR_INTERVAL_STR, REPEAT_DELAY_SECONDS)

            sleep = float(delay) - time.time() + start
            if sleep > 0:
                time.sleep(sleep)

    except KeyboardInterrupt:
        logging.info('Stopped by user')
        db.close_connection()

if __name__ == '__main__':
    args = parser.parse_args()
    global adc
    adc = adc_.create(ADC_TYPE)

    if args.calibrate:
        for i, _ in enumerate(SENSOR_TYPES):
            calibrate(i)
    else:
        run()
