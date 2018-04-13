# Simplified Version
 
import spidev
import time
import sys
import logging
import urllib2
import urllib
import re

#Start Log file
logging.basicConfig(filename="gasreadings.log", format = '%(asctime)-15s %(message)s', level=logging.INFO)

#Define Variables
delay = 240
cal_delay = 0.01

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


    print("Start Calibration for MQ2.")
    logging.info("Start Calibration for MQ2.")

    val1 = 0.0
    for i in range(50):
        val1 += readadc(0)
        time.sleep(cal_delay)

    val1 = val1/50

    if val1 == 0:
        val1 = val1 + 0.0000001

    Ro1 = (((1023/val1) - 1) * 5)/9.48

    print val1
    print Ro1
    logging.info("Ro for MQ-2 %g" % (Ro1))

    print("Start Calibration for MQ9.")
    logging.info("Start Calibration for MQ9.")

    val2 = 0.0
    for i in range(50):
        val2 += readadc(1)
        time.sleep(cal_delay)

    val2 = val2/50

    if val2 == 0:
        val2 = val2 + 0.0000001

    Ro2 = (((1023/val2) - 1) * 18)/9.71

    print val2
    print Ro2
    logging.info("Ro for MQ-9 %g" % (Ro2))

    print("Start Calibration for MQ135.")
    logging.info("Start Calibration for MQ135.")

    val3 = 0.0
    for i in range(50):
        val3 += readadc(2)
        time.sleep(cal_delay)

    val3 = val3/50

    if val3 == 0:
        val3 = val3 + 0.0000001

    Ro3 = (((1023/val3) - 1) * 20)/3.59

    print val3
    print Ro3
    logging.info("Ro for MQ-135 %g" % (Ro3))

    while True:
        output = urllib2.urlopen('http://54.244.200.105/globalValue?action=get&key=reading-frequency').read()
        online_delay = re.search(" is '(.+?)' the p", output).group(1)
        delay = float(online_delay)

        print '\n'
        print delay
        
        logging.info("Delay %g" % (delay))
       
        pin_one = readadc(0)
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("MQ-2 %g" % (pin_one))

        url1 = url + deviceId + '&instant=now&latitude=' + str(lat) + '&longitude=' + str(lon) + '&sensorType=' + sensorType1 + '&reading=' + str(pin_one) + '&ro=' + str(Ro1)
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

        url2 = url + deviceId + '&instant=now&latitude=' + str(lat) + '&longitude=' + str(lon) + '&sensorType=' + sensorType2 + '&reading=' + str(pin_two) + '&ro=' + str(Ro2)
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

        url3 = url + deviceId + '&instant=now&latitude=' + str(lat) + '&longitude=' + str(lon) + '&sensorType=' + sensorType3 + '&reading=' + str(pin_three) + '&ro=' + str(Ro3)
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
