"""Script to periodically read sensors and post readings to a Web site"""

import logging
import time

from config import DELAY_SECONDS, SENSOR_TYPES_WITH_INDEX
from utils import read_and_send_http


try:
    print('Press CTRL+C to abort')
    logging.info('Program started')

    while True:
        for sensor_type in SENSOR_TYPES_WITH_INDEX:
            read_and_send_http(sensor_type)
            time.sleep(DELAY_SECONDS)
except KeyboardInterrupt:
    print('\nAbort by user')
    logging.info('Program ended')
