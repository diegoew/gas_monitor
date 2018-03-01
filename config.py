REPEAT_DELAY_SECONDS = 60
SENSOR_TYPE_TO_PIN_NUM = {'MQ-2': 1, 'MQ-9': 2, 'MQ-135': 3}
DEVICE_ID = 'RaspPi-Prototype-1'
LAT = '34.0376455'
LON = '-118.437404'
BASE_URL = 'http://54.244.200.105/readings/calculate'

import logging
logging.basicConfig(filename="gas_readings.log",
                    format='%(asctime)-15s %(message)s',
                    level=logging.INFO)
