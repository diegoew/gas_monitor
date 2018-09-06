import time
import logging

import requests

from config import WEATHER_URL, OPENWEATHER_KEY, LAT, LON, \
    WEATHER_RETRIEVAL_INTERVAL_SECONDS


UNIT_TYPE = 'metric'  # imperial, metric or kelvin (default)
temperature = None
rel_humidity = None
timeout = 0


def _set_openweather():
    global temperature, rel_humidity, timeout
    params = dict(lat=LAT,
                  lon=LON,
                  appid=OPENWEATHER_KEY,
                  units=UNIT_TYPE,
                  mode='json')
    try:
        response = requests.get(WEATHER_URL, params=params)
        response.raise_for_status()
        parsed = response.json()['main']
    except Exception as e:
        logging.error('Failed to get weather: %s', e)
        return
    temperature = parsed['temp']
    rel_humidity = parsed['humidity'] / 100.0
    timeout = time.time() + WEATHER_RETRIEVAL_INTERVAL_SECONDS


def get_temperature_and_rel_humidity():
    if temperature is None or rel_humidity is None or timeout < time.time():
        _set_openweather()
    return temperature, rel_humidity
