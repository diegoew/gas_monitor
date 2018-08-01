import time

import requests

from config import WEATHER_URL, OPENWEATHER_KEY, LAT, LON, \
    WEATHER_RETRIEVAL_INTERVAL_SECONDS


UNIT = 'metric' # Possible values: kelvin, imperial, metric. Default is kelvin
temperature = None
rel_humidity = None
timeout = 0


def _set_openweather():
    global temperature, rel_humidity, timeout
    params = dict(lat=LAT,
                  lon=LON,
                  apiid=OPENWEATHER_KEY,
                  units=UNIT,
                  mode='json')
    parsed = requests.get(WEATHER_URL, params=params).json()['main']
    temperature = parsed['temp']
    rel_humidity = parsed['humidity']/100
    timeout = time.time() + WEATHER_RETRIEVAL_INTERVAL_SECONDS


def get_temperature_and_rel_humidity():
    if temperature is None or rel_humidity is None or timeout < time.time():
        _set_openweather()
    return temperature, rel_humidity
