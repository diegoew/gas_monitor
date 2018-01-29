# Simplified Version
 
import spidev
import time
import sys
import logging
import urllib2
import urllib

#Start Log file
logging.basicConfig(filename="gasreadings.log", format = '%(asctime)-15s %(message)s', level=logging.INFO)

#Define Variables
delay = 5

#Website Info
sensorType1 = 'MQ-2'
sensorType2 = 'MQ-9'
sensorType3 = 'MQ-135'
deviceId = 'RaspPi-Prototype-1'
lat = 34.0376455
lon = -118.437404
url = 'http://54.244.200.105/readings/calculate?deviceId='

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
    logging.info("Program Started")

    while True:
        pin_one = readadc(0)
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("MQ-2 %g" % (pin_one))

        url1 = url + deviceId + '&instant=now&latitude=' + str(lat) + '&longitude=' + str(lon) + '&sensorType=' + sensorType1 + '&reading=' + str(pin_one)
        query_args1 = {}
        data1 = urllib.urlencode(query_args1)
        request1 = urllib2.Request(url1, data1)
        response1 = urllib2.urlopen(request1)
        
        logging.info("MQ-2 %g" % (pin_one))

        sys.stdout.flush()
        time.sleep(delay)

        pin_two = readadc(1)
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("MQ-9 %g" % (pin_two))

        url2 = url + deviceId + '&instant=now&latitude=' + str(lat) + '&longitude=' + str(lon) + '&sensorType=' + sensorType2 + '&reading=' + str(pin_two)
        query_args2 = {}
        data2 = urllib.urlencode(query_args2)
        request2 = urllib2.Request(url2, data2)
        response2 = urllib2.urlopen(request2)
        
        logging.info("MQ-9 %g" % (pin_two))

        sys.stdout.flush()
        time.sleep(delay)

        pin_three = readadc(2)
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("MQ-135 %g" % (pin_three))

        url3 = url + deviceId + '&instant=now&latitude=' + str(lat) + '&longitude=' + str(lon) + '&sensorType=' + sensorType3 + '&reading=' + str(pin_three)
        query_args3 = {}
        data3 = urllib.urlencode(query_args3)
        request3 = urllib2.Request(url3, data3)
        response3 = urllib2.urlopen(request3)
        
        logging.info("MQ-135 %g" % (pin_three))

        sys.stdout.flush()
        time.sleep(delay)    

except:
    print("\nAbort by user")
    logging.info("Program Ended")
