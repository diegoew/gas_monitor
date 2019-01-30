DEVICE_ID =   # Unique name for this device

# Geographic position. You can find it using http://maps.google.com
LAT = #34.0376455
LON = #-118.437404

ADC_TYPE = 'ads1115'  # ads1115 or mcp3008
SENSOR_TYPES = ['MQ-2', 'MQ-9', 'MQ-135']  # Sensors connected to each pin

OPENWEATHER_KEY =  #'177f943c86860b2efb332b00962ac509'
# From https://home.openweathermap.org/api_keys
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'
WEATHER_RETRIEVAL_INTERVAL_SECONDS = 60

REPEAT_DELAY_SECONDS = 60
DB = 'readings.sqlite'
SERVER_URL = 'http://34.223.248.143/readings/calculate'

import logging
logging.basicConfig(filename="readings.log",
                    format='%(asctime)-15s %(message)s',
                    level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())