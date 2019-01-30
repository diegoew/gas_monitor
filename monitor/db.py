from datetime import datetime
import logging
import os
import sqlite3

from config import DB


DB_TABLE = 'readings'

connection = None


def get_connection():
    global connection
    if not connection:
        connection = sqlite3.connect(DB)
    return connection


def close_connection():
    if connection:
        try:
            connection.close()
        except:
            pass


def init():
    if not os.path.isfile(DB):
        cursor = get_connection().cursor()
        cursor.executescript('''
        CREATE TABLE readings(
            id INTEGER NOT NULL PRIMARY KEY,
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sensor VARCHAR(8),
            reading FLOAT,
            ro FLOAT NULL,
            temperature FLOAT NULL,
            rel_humidity FLOAT NULL,
            upload_ts TIMESTAMP NULL
        );
        CREATE TABLE ros(
            id INTEGER NOT NULL PRIMARY KEY,
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sensor VARCHAR(8),
            ro FLOAT
        );''')


def store_reading(ts, sensor_type, reading, ro, temperature=None,
                      rel_humidity=None, upload_ts=None):
    cursor = get_connection().cursor()
    try:
        cursor.execute(
            'INSERT INTO %s' % DB_TABLE
            + '(ts, sensor, reading, ro, temperature, rel_humidity, upload_ts)'
            + ' VALUES (?, ?, ?, ?, ?, ?, ?);',
            (ts, sensor_type, reading, ro, temperature, rel_humidity,
             upload_ts))
        get_connection().commit()
    except Exception as e:
        logging.error('Failed to record reading into DB: %s', e)


def get_not_uploaded():
    """Get all recorded readings that were not uploaded"""
    cursor = get_connection().cursor()
    # Get all recorded readings that were not uploaded
    try:
        cursor.execute('SELECT * FROM %s' % DB_TABLE
                       + '  WHERE upload_ts IS NULL ORDER BY ts ASC;')
        return cursor.fetchall()
    except Exception as e:
        logging.error('Failed to get recorded readings: %s', e)
        return


def record_uploaded_time(id_):
    """Record uploaded time. Throws exceptions on error."""
    cursor = get_connection().cursor()
    cursor.execute('UPDATE %s' % DB_TABLE
                   + ' SET upload_ts = ? WHERE id = ?;',
                   (datetime.now(), id_))
    get_connection().commit()


def get_ro(sensor_type):
    cursor = get_connection().cursor()
    cursor.execute('SELECT ro FROM ros WHERE sensor = ?'
                   ' ORDER BY ts DESC LIMIT 1;', [sensor_type])
    res = cursor.fetchone()
    if res is not None:
        return res[0]


def store_ro(sensor_type, ro):
    cursor = get_connection().cursor()
    cursor.execute('INSERT INTO ros (sensor, ro) values (?, ?);',
                   [sensor_type, ro])
    get_connection().commit()
