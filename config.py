DEVICE_ID = 'RaspPi-Prototype-1'
LAT = '34.0376455'
LON = '-118.437404'
SERVER_URL = 'http://34.223.248.143/readings/calculate'
REPEAT_DELAY_SECONDS = 60
SENSOR_TYPES = ['MQ-2', 'MQ-9', 'MQ-135']
LOAD_RESISTANCES = [5, 18, 20]
AIR_RESISTANCE_RATIOS = [9.48, 9.71, 3.59]


import logging
logging.basicConfig(filename="gas_readings.log",
                    format='%(asctime)-15s %(message)s',
                    level=logging.INFO)
