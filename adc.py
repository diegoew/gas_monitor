import logging

import spidev

from config import SENSOR_TYPES
from sensors import LOAD_RESISTANCES, RSCO_RO_RATIOS


class Adc:
    RESOLUTION = 0

    def read(self, pin_num):
        assert isinstance(pin_num, int) and 0 <= pin_num < len(SENSOR_TYPES), \
            'Invalid pin number: %s' % pin_num

    def calibrate(self, pin_num):
        """Calibrate sensor.
        :return Ro, the calculated sensor resistance for the given sensor type

        Ro as the sensor resistance at a specific calibration gas. It was defined by
        sensor manufacturer (see the data sheet linked from the README document).
        But because we do not have pure gases available, we approximate Ro using Rs,
        the resistance at various concentrations of gases, and the ratio Rs/Ro which
        is almost constant for pure air and is given by the manufacturer.
        """
        sensor_type = SENSOR_TYPES[pin_num]
        logging.info('Calibrate ' + sensor_type)

        val = 0.0
        for _ in range(50):
            val += self.read(pin_num)
        val /= 50

        if val == 0:
            val += 0.0000001

        lr = LOAD_RESISTANCES[sensor_type]
        arr = RSCO_RO_RATIOS[sensor_type]
        ro = (self.RESOLUTION / val - 1) * lr / arr

        logging.info('Ro=%g', ro)

        return ro


class Mcp3008(Adc):
    """
    An 8-channel, 11-bit analog-to-digital converter. It supports negative
    values, so we use 10 bits. So the resolution is 2^10 - 1 = 1023 values.
    """
    RESOLUTION = 1023

    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)

    def read(self, pin_num):
        """
        :return SPI data from the MCP3008 analogue-to-digital converter (ADC),
        from 8 channels in total.
        """
        Adc.read(self, pin_num)
        r = self.spi.xfer2([1, 8 + pin_num << 4, 0])
        return ((r[1] & 3) << 8) + r[2]


class Ads1115(Adc):
    """
    An 8-channel, 16-bit analog-to-digital converter. It supports negative
    values, but sensors only supply positive values. So the resolution is 16 - 1
    = 15 bits, or 2^15 - 1 = 32767 values.
    """
    RESOLUTION = 32767
    GAIN = 2 / 3  # For reading voltages from -6.144V to +6.144V.

    def __init__(self):
        import Adafruit_ADS1x15
        self.adafruit = Adafruit_ADS1x15.ADS1115()

    def read(self, pin_num):
        Adc.read(self, pin_num)
        return self.adafruit.read_adc(pin_num, gain=self.GAIN)


def create(adc_type):
    adc_type = adc_type.lower()
    if adc_type == 'mcp3008':
        return Mcp3008()
    if adc_type == 'ads1115':
        return Ads1115()