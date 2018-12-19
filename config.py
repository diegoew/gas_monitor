DEVICE_ID = 'RaspPi-Prototype-1'
LAT = '34.0376455'
LON = '-118.437404'
SERVER_URL = 'http://34.223.248.143/readings/calculate'
REPEAT_DELAY_SECONDS = 60
SENSOR_TYPES = ['MQ-2', 'MQ-9', 'MQ-135']
ADS1115_GAIN = 2/3  # For reading voltages from -6.144V to +6.144V.
LOAD_RESISTANCES = [5, 18, 20]
AIR_RESISTANCE_RATIOS = [9.48, 9.71, 3.59]
DB = 'measurements.sqlite'
ADC_RESOLUTION = 32767  # 32767 for ADS, 1023 for MCP
DB_TABLE = 'measurements'
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather'
# Unique key per Gas Monitor, can be used up to 60 times per minute
OPENWEATHER_KEY = '177f943c86860b2efb332b00962ac509'
WEATHER_RETRIEVAL_INTERVAL_SECONDS = 60

import logging
logging.basicConfig(filename="measurements.log",
                    format='%(asctime)-15s %(message)s',
                    level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())