import logging
import sys
import time

import requests
import spidev

from config import BASE_URL, DEVICE_ID, LAT, LON, SENSOR_TYPES_WITH_INDEX

spi = spidev.SpiDev()
spi.open(0, 0)


def read_adc(sensor_type):
    """Read SPI data from the MCP3008, 8 channels in total"""
    adc_num = SENSOR_TYPES_WITH_INDEX[sensor_type]
    if not 0 <= adc_num <= 7:
        return -1
    r = spi.xfer2([1, 8 + adc_num << 4, 0])
    return ((r[1] & 3) << 8) + r[2]


def calibrate(sensor_type):
    """Calibrate sensor"""
    print('Start calibration for', sensor_type)
    logging.info('Start calibration for', sensor_type)

    val = 0.0
    for _ in range(50):
        val += read_adc(sensor_type)
        time.sleep(5 / 1000)

    val /= 50
    if val == 0:
        val += 0.0000001

    ro = (1023 / val - 1) * 5 / 9.48

    print('Ro', ro)
    logging.info('Ro', ro)

    return ro


def read_and_send_http(sensor_type, ro=None):
    reading = read_adc(sensor_type)
    sys.stdout.write('\r\033[K%s %g' % (sensor_type, reading))
    params = dict(
        device_id=DEVICE_ID,
        instant='now',
        latitude=LAT,
        longitude=LON,
        sensorType=sensor_type,
        reading=reading,
    )
    if ro is not None:
        params['ro'] = ro
    requests.get(BASE_URL, params=params)
    sys.stdout.flush()