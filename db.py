from datetime import datetime
import logging
import os
import sqlite3

from config import DB, DB_TABLE


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
        CREATE TABLE measurements(
            id INT AUTO_INCREMENT PRIMARY KEY,
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sensor VARCHAR(8),
            reading FLOAT,
            ro FLOAT NULL,
            temperature FLOAT NULL,
            rel_humidity FLOAT NULL,
            upload_ts TIMESTAMP NULL
        );
        CREATE TABLE ros(
            id INT AUTO_INCREMENT PRIMARY KEY,
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            MQ2 FLOAT,
            MQ9 FLOAT,
            MQ135 FLOAT
        );''')


def store_measurement(ts, sensor_type, reading, ro, temperature=None,
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
        logging.error('Failed to record measurement into DB: %s', e)


def get_not_uploaded():
    """Get all recorded measurements that were not uploaded"""
    cursor = get_connection().cursor()
    # Get all recorded measurements that were not uploaded
    try:
        cursor.execute('SELECT * FROM %s' % DB_TABLE
                       + '  WHERE upload_ts IS NULL ORDER BY ts ASC;')
        return cursor.fetchall()
    except Exception as e:
        logging.error('Failed to get recorded measurements')
        return


def record_uploaded_time(id_):
    """Record uploaded time. Throws exceptions on error."""
    cursor = get_connection().cursor()
    cursor.execute('UPDATE %s' % DB_TABLE
                   + ' SET upload_ts = ? WHERE id = ?;',
                   (datetime.now(), id_))
    get_connection().commit()


def get_ros():
    cursor = get_connection().cursor()
    cursor.execute('SELECT MQ2, MQ9, MQ135 FROM ros'
                   ' ORDER BY ts DESC LIMIT 1;')
    return cursor.fetchone()


def store_ros(mq_2, mq_9, mq_135):
    cursor = get_connection().cursor()
    cursor.execute('INSERT INTO ros (MQ2, MQ9, MQ135) values (?, ?, ?);',
                   [mq_2, mq_9, mq_135])
    get_connection().commit()
