"""Script to read sensors and print readings to the screen"""

import time

from config import DELAY_SECONDS, SENSOR_TYPES_WITH_INDEX
from utils import read_adc


try:
    print('Press Ctrl+C to abort.')

    while True:
        pins = (read_adc(t) for t in SENSOR_TYPES_WITH_INDEX)
        print ('---------------------------------------')
        print('CH0 %g, CH1 %g, CH2 %g' % pins)
        time.sleep(DELAY_SECONDS)
except KeyboardInterrupt:
    print('\nAbort by user')
