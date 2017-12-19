# Simplified Version
 
import spidev
import time
import sys

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

try:
    print("Press CTRL+C to abort.")    

    while True:
    	pin_one = readadc(0)
    	pin_two = readadc(1)
    	pin_three = readadc(2)
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("CH0 %g, CH1 %g, CH2 %g" % (pin_one, pin_two, pin_three))
        sys.stdout.flush()
        time.sleep(delay)

except:
    print("\nAbort by user")

