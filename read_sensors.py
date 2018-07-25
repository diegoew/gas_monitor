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
    SENSOR_TYPE_TO_PIN_NUM, SENSOR_TYPE_TO_LOAD_RESISTANCE, \
    SENSOR_TYPE_TO_AIR_RESISTANCE_RATIO, DB_HOST, DB_USER, DB_PASSWORD, DB, \
    DB_TABLE


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

parser = argparse.ArgumentParser(
    description='Read gas sensors ' + ', '.join(SENSOR_TYPE_TO_PIN_NUM)
    + '\nTo configure, edit file config.py.'
)

db_connection = None
spi = spidev.SpiDev()
spi.open(0, 0)


def get_db_connection():
    global db_connection
    if not db_connection or not db_connection.open:
        db_connection = pymysql.connect(host=DB_HOST,
                                        user=DB_USER,
                                        password=DB_PASSWORD,
                                        db=DB,
                                        autocommit=True)
    return db_connection


def read_adc(sensor_type):
    """
    :return SPI data from the MCP3008 analogue-to-digital converter (ADC),
    from 8 channels in total.
    """
    adc_num = SENSOR_TYPE_TO_PIN_NUM[sensor_type]
    if not 0 <= adc_num <= 7:
        return -1
    r = spi.xfer2([1, 8 + adc_num << 4, 0])
    return ((r[1] & 3) << 8) + r[2]


def calibrate(sensor_type):
    """Calibrate sensor.
    :return Ro, the calculated sensor resistance for the given sensor type

    Ro as the sensor resistance at a specific calibration gas. It was defined by
    sensor manufacturer (see the data sheet linked from the README document).
    But because we do not have pure gases available, we approximate Ro using Rs,
    the resistance at various concentrations of gases, and the ratio Rs/Ro which
    is almost constant for pure air and is given by the manufacturer.
    """
    print('Calibrate ' + sensor_type)
    logging.info('Calibrate ' + sensor_type)

    val = 0.0
    for _ in range(50):
        val += read_adc(sensor_type)
    val /= 50

    if val == 0:
        val += 0.0000001

    lr = SENSOR_TYPE_TO_LOAD_RESISTANCE[sensor_type]
    arr = SENSOR_TYPE_TO_AIR_RESISTANCE_RATIO[sensor_type]
    ro = (1023 / val - 1) * lr / arr

    print('Val:', val, 'Ro:', ro)
    logging.info('Ro=%g' % ro)

    return ro


def timestamp():
    td_str = datetime.now(timezone.utc).astimezone().strftime(DATETIME_FORMAT)
    return td_str[:-2] + ':' + td_str[-2:]


def upload(sensor_type, reading, ro=None, ts=None):
    data = dict(
        deviceId=DEVICE_ID,
        instant=ts or timestamp(),
        latitude=LAT,
        longitude=LON,
        sensorType=sensor_type,
        reading=reading,
    )
    if ro is not None:
        data['ro'] = ro
    response = requests.post(SERVER_URL, data=data)
    response.raise_for_status()


def record(sensor_type, reading, ro, error_str):
    with get_db_connection().cursor() as cursor:
        try:
            cursor.execute(
                'INSERT INTO %s(ts, sensor, reading, ro, upload_error)' % DB_TABLE
                + ' VALUES (%s, %s, %s, %s, %s);',
                (datetime.now(), sensor_type, reading, ro, error_str[:100]))
        except Exception as e:
            logging.error('Failed to record reading into DB:' , e)


def upload_recorded():
    with get_db_connection().cursor() as cursor:
        # Get all recorded measurements that were not uploaded
        try:
            cursor.execute(
                'SELECT * FROM %s WHERE upload_ts IS NULL' % DB_TABLE
                + ' ORDER BY ts ASC;')
        except Exception as e:
            logging.error('Failed to get recorded measurements')
            return

        # Upload and record the upload timestamp for each measurement
        for id_, ts, sensor, reading, ro, _, _ in cursor.fetchall():
            try:
                upload(sensor, reading, ro, ts=ts)
            except Exception as e:
                logging.error('Failed to upload recorded measurement %s: %s' %
                              (id_, e))
                continue
            try:
                cursor.execute('UPDATE %s' % DB_TABLE
                               + ' SET upload_ts = %s WHERE id = %s;', 
                               (datetime.now(), id_))
            except Exception as e:
                logging.error('Failed to record the upload timestamp for'
                              ' meaurement %s: %s' % (id_, e))
                break


def run(should_calibrate=True):
    try:
        print('Press Ctrl+C to abort')
        logging.info('Program started')

        if should_calibrate:
            ros = [calibrate(t) for t in SENSOR_TYPE_TO_PIN_NUM]
        else:
            ros = [None, None, None]

        print('\nRead sensors every %s seconds...' % REPEAT_DELAY_SECONDS)
        while True:
            upload_recorded()

            sys.stdout.write('\r\033[K')
            for sensor_type, ro in zip(SENSOR_TYPE_TO_PIN_NUM, ros):
                val = read_adc(sensor_type)
                sys.stdout.write('%s:%g ' % (sensor_type, val))
                sys.stdout.flush()

                try:
                    upload(sensor_type, val, ro)
                except requests.exceptions.ConnectionError as e:
                    record(cursor, sensor_type, val, ro,
                           'Could not connect to ' + SERVER_URL)
                except requests.exceptions.HTTPError as e:
                    if hasatr(e, 'args') and len(e.args) > 0:
                        err_str = e.args[0]
                    else:
                        err_str = str(e)
                    record(cursor, sensor_type, val, ro, err_str)
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
