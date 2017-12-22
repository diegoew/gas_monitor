# Simplified Version
 
import spidev
import time
import sys
from .client.config import Config
from .client.webService import WebService
import pprint as pp

#Define Variables
delay = 1

#Create SPI
spi = spidev.SpiDev()
spi.open(0, 0)
 
def readadc(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

def run():
    config = Config()

    web = WebService(config)

    try:
        print("Press CTRL+C to abort.")

        while True:
            # Get Readings
    	    MQ_2 = readadc(0)
    	    MQ_9 = readadc(1)
    	    MQ_135 = readadc(2)

            # Post readings
            web.postReading("MQ-2", MQ_2)
            web.postReading("MQ-9", MQ_9)
            web.postReading("MQ-135", MQ_135)

            # Display Readings
            sys.stdout.write("\r")
            sys.stdout.write("\033[K")
            sys.stdout.write("CH0 %g, CH1 %g, CH2 %g" % (MQ_2, MQ_9, MQ_135))
            sys.stdout.flush()

            time.sleep(delay)

    except:
        print("\nAbort by user")

if __name__ == "__main__":
    run()

