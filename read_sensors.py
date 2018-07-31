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

import pymysql
import requests
import spidev

from config import REPEAT_DELAY_SECONDS, SERVER_URL, DEVICE_ID, LAT, LON, \
    SENSOR_TYPES, LOAD_RESISTANCES, AIR_RESISTANCE_RATIOS \
    DB_HOST, DB_USER, DB_PASSWORD, DB, DB_TABLE

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

parser = argparse.ArgumentParser(
    description='Read gas sensors ' + ', '.join(SENSOR_TYPES)
    + '\nTo configure, edit file config.py.'
)

db_connection = None
spi = spidev.SpiDev()


def get_db_connection():
    global db_connection
    if not db_connection or not db_connection.open:
        db_connection = pymysql.connect(host=DB_HOST,
                                        user=DB_USER,
                                        password=DB_PASSWORD,
                                        db=DB,
                                        autocommit=True)
    return db_connection


def read_adc(pin_num):
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


def timestamp(dt):
    td_str = dt.strftime(DATETIME_FORMAT)
    return td_str[:-2] + ':' + td_str[-2:]


def upload(dt, sensor_type, reading, ro=None):
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
    response = requests.post(SERVER_URL, data=data)
    response.raise_for_status()


def record(ts, sensor_type, reading, ro, upload_ts=None):
    with get_db_connection().cursor() as cursor:
        try:
            cursor.execute(
                'INSERT INTO %s' % DB_TABLE
                + '(ts, sensor, reading, ro, upload_ts)'
                + ' VALUES (%s, %s, %s, %s, %s);',
                (ts, sensor_type, reading, ro, upload_ts))
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
        for id_, dt, sensor_type, reading, ro, _ in cursor.fetchall():
            try:
                upload(dt, sensor_type, reading, ro)
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
                dt = datetime.now(timezone.utc).astimezone()
                sys.stdout.write('%s:%g ' % (sensor_type, val))
                sys.stdout.flush()
                record(dt, sensor_type, val, ro)
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
