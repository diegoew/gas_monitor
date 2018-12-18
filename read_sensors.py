#!/usr/bin/env python3
"""
Script to periodically read gas concentration measurements from sensors,
record them to a local database and upload them to a Web service.
"""
import argparse
from datetime import datetime, timezone
import logging
import sys
import time

import requests

from config import REPEAT_DELAY_SECONDS, SERVER_URL, DEVICE_ID, LAT, LON, \
    SENSOR_TYPES
import db
import openweather
import ads1115 as sensors


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

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
    """Format the datetime dt to a string that includes time zone offset.
    If dt is not zone aware, use the OS offset."""
    dt_str = dt.strftime(DATETIME_FORMAT)
    tz_str = dt.strftime('%z') \
             or datetime.now(timezone.utc).astimezone().strftime('%z')
    return dt_str + tz_str[:-2] + ':' + tz_str[-2:]


def upload(dt, sensor_type, reading, ro=None, temperature=None,
           rel_humidity=None):
    data = dict(
        deviceId=DEVICE_ID,
        instant=timestamp(dt),
        latitude=LAT,
        longitude=LON,
        sensorType=sensor_type,
        reading=reading,
    )
    if ro is not None:
        data['ro'] = ro
    if temperature is not None:
        data['temperature'] = temperature
    if rel_humidity is not None:
        data['rel_humidity'] = rel_humidity
    response = requests.post(SERVER_URL, data=data)
    response.raise_for_status()


def upload_recorded():
        not_uploaded = db.get_not_uploaded()
        # Upload each measurement and record its upload timestamp
        for id_, dt, sensor_type, reading, ro, temperature, rel_humidity, _ \
                in not_uploaded:
            try:
                upload(dt, sensor_type, reading, ro, temperature, rel_humidity)
            except Exception as e:
                logging.error('Failed to upload measurement %s: %s', id_, e)
                break

            try:
                db.record_uploaded_time(id_)
            except Exception as e:
                logging.error('Failed to record the upload timestamp for'
                              ' measurement %s: %s', id_, e)
                break


def get_ros():
    ros = db.get_ros()
    if not ros:
        ros = calibrate()
    return ros


def calibrate():
    ros = [sensors.calibrate(i) for i in range(len(SENSOR_TYPES))]
    db.store_ros(*ros)
    return ros


def run():
    sensors.init()

    try:
        logging.info('\nProgram started. Press Ctrl+C to stop')

        ros = get_ros()

        logging.info('\nRead sensors every %s seconds...' % REPEAT_DELAY_SECONDS)
        while True:
            sys.stdout.write('\r\033[K')
            for pin_num, (sensor_type, ro) in enumerate(zip(SENSOR_TYPES, ros)):
                val = sensors.read(pin_num)
                dt = datetime.now(timezone.utc).astimezone()
                sys.stdout.write('%s:%g ' % (sensor_type, val))
                sys.stdout.flush()
                temp, hum = openweather.get_temperature_and_rel_humidity()
                db.store_measurement(dt, sensor_type, val, ro, temp, hum)
                upload_recorded()
                time.sleep(REPEAT_DELAY_SECONDS)

    except KeyboardInterrupt:
        logging.info('Stopped by user')
        db.close_connection()

if __name__ == '__main__':
    args = parser.parse_args()
    if args.calibrate:
        calibrate()
    else:
        run()
