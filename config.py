DEVICE_ID = 'RaspPi-Prototype-1'
LAT = '34.0376455'
LON = '-118.437404'
SERVER_URL = 'http://34.223.248.143/readings/calculate'
REPEAT_DELAY_SECONDS = 60
SENSOR_TYPE_TO_PIN_NUM = {
    'MQ-2': 1, 'MQ-9': 2, 'MQ-135': 3
}
SENSOR_TYPE_TO_LOAD_RESISTANCE = {
    'MQ-2': 5, 'MQ-9': 18, 'MQ-135': 20
}
SENSOR_TYPE_TO_AIR_RESISTANCE_RATIO = {
    'MQ-2': 9.48, 'MQ-9': 9.71, 'MQ-135': 3.59
}


import logging
logging.basicConfig(filename="gas_readings.log",
                    format='%(asctime)-15s %(message)s',
                    level=logging.INFO)
