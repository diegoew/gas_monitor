#!/usr/bin/env python3
"""
Periodically reads gas concentration data from the local database that were not
uploaded and uploads them to the Web service.
"""
import logging
import re
import requests
import time

import db
from config import SECONDS_BETWEEN_UPLOAD_RETRIES, SERVER, DEVICE_ID, LAT, LON


SECONDS_BETWEEN_READINGS_JSON_KEY = 'secondsBetweenReadings'


dt_format = r'(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})' \
            r' (?P<time>[0-9]{2}:[0-9]{2}:[0-9]{2})' \
            r'(.[0-9]{6})?' \
            r'(?P<tz>-[0-9]{2}:[0-9]{2})'
dt_re = re.compile(dt_format)


def timestamp(dt):
    """Assume a timestring with format yyyy-mm-dd HH:MM:SS.uuuuuu-hh:mm.
    Return a timestring with format yyyy-mm-ddTHH:MM:SS-hh:mm
    Example:
        input:  2018-12-18 22:23:35.901293-08:00
        output: 2018-12-18T22:23:35-08:00
        """
    m = dt_re.match(dt)
    return m.group('date') + 'T' + m.group('time') + m.group('tz')


def upload(ts, sensor_type, reading, resolution, ro=None, temperature=None,
           humidity=None):
    data = dict(
        deviceId=DEVICE_ID,
        instant=timestamp(ts),
        latitude=LAT,
        longitude=LON,
        sensorType=sensor_type,
        reading=reading,
        resolution=resolution,
    )
    if ro is not None:
        data['ro'] = ro
    if temperature is not None:
        data['tempInCelsius'] = temperature
    if humidity is not None:
        data['relativeHumidity'] = humidity
    response = requests.post('http://%s/readings/calculate' % SERVER, data=data)
    if not response.ok:
        logging.error('Failed to upload %s %s: %s'
                      % (ts, sensor_type, response.status_code))
    try:
        db.record_uploaded_time(ts, sensor_type)
    except Exception as e:
        logging.error('Failed to record the upload timestamp for reading '
                      '%s %s: %s' % (ts, sensor_type, e))
    return response.headers.get(SECONDS_BETWEEN_READINGS_JSON_KEY)


def upload_recorded():
        delay = None
        not_uploaded = db.get_not_uploaded()

        # Upload each reading and record its upload timestamp
        for dt, sensor_type, val, res, ro, temp, hum, _ in not_uploaded:
                delay = upload(str(dt), sensor_type, val, res, ro, temp, hum)
        return delay


def run():
    try:
        while True:
            upload_recorded()
            time.sleep(SECONDS_BETWEEN_UPLOAD_RETRIES)

    except KeyboardInterrupt:
        logging.info('Keyboard interrupt')
        db.close_connection()

if __name__ == '__main__':
    run()
