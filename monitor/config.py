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

DEFAULT_SECONDS_BETWEEN_READINGS = 60
SERVER_URL = 'http://34.223.248.143/readings/calculate'


import inspect
import logging
import os
os.chdir(os.path.dirname(inspect.getfile(inspect.currentframe())))
logging.basicConfig(handlers=[logging.StreamHandler()],
                    format='%(levelname)s %(message)s',
                    level=logging.INFO)
