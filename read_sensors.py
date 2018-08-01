#!/usr/bin/env python
"""
Script to periodically read gas concentration measurements from sensors,
record them to a local database and upload them to a Web service.
"""
import argparse
from datetime import datetime, timezone
import logging
import sys
import time

import pymysql
import requests

from config import REPEAT_DELAY_SECONDS, SERVER_URL, DEVICE_ID, LAT, LON, \
    SENSOR_TYPES, DB_HOST, DB_USER, DB_PASSWORD, DB, DB_TABLE
import openweather
import sensor


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

parser = argparse.ArgumentParser(
    description='Read gas sensors ' + ', '.join(SENSOR_TYPES)
    + '\nTo configure, edit file config.py.'
)

db_connection = None


def get_db_connection():
    global db_connection
    if not db_connection or not db_connection.open:
        db_connection = pymysql.connect(host=DB_HOST,
                                        user=DB_USER,
                                        password=DB_PASSWORD,
                                        db=DB,
                                        autocommit=True)
    return db_connection


def timestamp(dt):
    td_str = dt.strftime(DATETIME_FORMAT)
    return td_str[:-2] + ':' + td_str[-2:]


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


def record(ts, sensor_type, reading, ro, temperature=None, rel_humidity=None,
           upload_ts=None):
    with get_db_connection().cursor() as cursor:
        try:
            cursor.execute(
                'INSERT INTO %s' % DB_TABLE
                + '(ts, sensor, reading, ro, upload_ts)'
                + ' VALUES (%s, %s, %s, %s, %s, %s, %s);',
                (ts, sensor_type, reading, ro, temperature, rel_humidity,
                 upload_ts))
        except Exception as e:
            logging.error('Failed to record measurement into DB:', e)


def upload_recorded():
    with get_db_connection().cursor() as cursor:
        # Get all recorded measurements that were not uploaded
        try:
            cursor.execute('SELECT * FROM %s' % DB_TABLE
                           + '  WHERE upload_ts IS NULL ORDER BY ts ASC;')
        except Exception as e:
            logging.error('Failed to get recorded measurements')
            return

        # Upload each measurement and record its upload timestamp
        for id_, dt, sensor_type, reading, ro, temperature, rel_humidity, _ \
                in cursor.fetchall():
            try:
                upload(dt, sensor_type, reading, ro, temperature, rel_humidity)
            except Exception as e:
                logging.error('Failed to upload measurement %s: %s', (id_, e))
                break

            try:
                cursor.execute('UPDATE %s' % DB_TABLE
                               + ' SET upload_ts = %s WHERE id = %s;', 
                               (datetime.now(), id_))
            except Exception as e:
                logging.error('Failed to record the upload timestamp for'
                              ' measurement %s: %s', (id_, e))
                break


def run():
    sensor.spi.open(0, 0)

    try:
        print('Press Ctrl+C to abort')
        logging.info('Program started')

        ros = [sensor.calibrate(i) for i in range(len(SENSOR_TYPES))]

        print('\nRead sensors every %s seconds...' % REPEAT_DELAY_SECONDS)
        while True:
            sys.stdout.write('\r\033[K')
            for pin_num, (sensor_type, ro) in enumerate(zip(SENSOR_TYPES, ros)):
                val = sensor.read_adc(pin_num)
                dt = datetime.now(timezone.utc).astimezone()
                sys.stdout.write('%s:%g ' % (sensor_type, val))
                sys.stdout.flush()
                temp, hum = openweather.get_temperature_and_rel_humidity()
                record(dt, sensor_type, val, ro, temp, hum)
                upload_recorded()
                time.sleep(REPEAT_DELAY_SECONDS)

    except KeyboardInterrupt:
        print('\nAbort by user')
        logging.info('Abort by user')
        if db_connection:
            try:
                db_connection.close()
            except:
                pass


if __name__ == '__main__':
    args = parser.parse_args()
    run()
