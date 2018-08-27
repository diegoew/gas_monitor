from datetime import datetime
import logging
import pymysql

from config import DB_HOST, DB_USER, DB_PASSWORD, DB, DB_TABLE


connection = None


def get_connection():
    global connection
    if not connection or not connection.open:
        connection = pymysql.connect(host=DB_HOST,
                                     user=DB_USER,
                                     password=DB_PASSWORD,
                                     db=DB,
                                     autocommit=True)
    return connection


def close_connection():
    if connection:
        try:
            connection.close()
        except:
            pass


def store_measurement(ts, sensor_type, reading, ro, temperature=None,
                      rel_humidity=None, upload_ts=None):
    with get_connection().cursor() as cursor:
        try:
            cursor.execute(
                'INSERT INTO %s' % DB_TABLE
                + '(ts, sensor, reading, ro, temperature, rel_humidity, upload_ts)'
                + ' VALUES (%s, %s, %s, %s, %s, %s, %s);',
                (ts, sensor_type, reading, ro, temperature, rel_humidity,
                 upload_ts))
        except Exception as e:
            logging.error('Failed to record measurement into DB: %s', e)
            print('Failed to record measurement into DB: %s' % e)


def get_not_uploaded():
    """Get all recorded measurements that were not uploaded"""
    with get_connection().cursor() as cursor:
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
    with get_connection().cursor() as cursor:
        cursor.execute('UPDATE %s' % DB_TABLE
                       + ' SET upload_ts = %s WHERE id = %s;',
                       (datetime.now(), id_))


def get_ros():
    with get_connection().cursor() as cursor:
        cursor.execute('SELECT MQ2, MQ9, MQ135 FROM ros'
                       ' ORDER BY ts DESC LIMIT 1;')
        return cursor.fetchone()


def store_ros(mq_2, mq_9, mq_135):
    with get_connection().cursor() as cursor:
        cursor.execute('INSERT INTO ros (MQ2, MQ9, MQ135) values (%s, %s, %s);',
                       [mq_2, mq_9, mq_135])
