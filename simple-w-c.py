"""
Script to calibrate sensors, then periodically read sensors and post
readings to a Web site
"""

import logging
import time

from config import DELAY_SECONDS, SENSOR_TYPES_WITH_INDEX
from utils import calibrate, read_and_send_http


try:
    print('Press Ctrl+C to abort')
    logging.info('Program started')

    ros = [calibrate(sensor_type) for sensor_type in SENSOR_TYPES_WITH_INDEX]

    while True:
        for sensor_type, ro in zip(SENSOR_TYPES_WITH_INDEX, ros):
            read_and_send_http(sensor_type, ro)
            time.sleep(DELAY_SECONDS)
except KeyboardInterrupt:
    print('\nAbort by user')
    logging.info('Program ended')
