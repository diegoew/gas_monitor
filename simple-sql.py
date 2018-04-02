# Simplified Version
 
import spidev
import time
import sys
import MySQLdb

#Time Variables
delay = 60

#Setup Info
sensorType1 = 'MQ-2'
sensorType2 = 'MQ-9'
sensorType3 = 'MQ-135'
deviceId = 'RaspPi-Prototype-1'

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

    print("Start Calibration for MQ2.")
    
    val1 = 0.0
    for i in range(50):
        val1 += readadc(0)
        time.sleep(0.1)

    val1 = val1/50

    if val1 == 0:
        val1 = val1 + 0.0000001

    Ro1 = (((1023/val1) - 1) * 5)/9.48

    print val1
    print Ro1

    print("Start Calibration for MQ9.")

    val2 = 0.0
    for i in range(50):
        val2 += readadc(1)
        time.sleep(0.1)

    val2 = val2/50

    if val2 == 0:
        val2 = val2 + 0.0000001

    Ro2 = (((1023/val2) - 1) * 18)/9.71

    print val2
    print Ro2

    print("Start Calibration for MQ135.")

    val3 = 0.0
    for i in range(50):
        val3 += readadc(2)
        time.sleep(0.1)

    val3 = val3/50

    if val3 == 0:
        val3 = val3 + 0.0000001

    Ro3 = (((1023/val3) - 1) * 20)/3.59

    print val3
    print Ro3

    while True:
    	pin_one = readadc(0)
    	pin_two = readadc(1)
    	pin_three = readadc(2)

    	db = MySQLdb.connect(host="localhost", user="root", passwd="stay-away-666", db="pythonspot")
    	cursor = db.cursor()
    	data = [
        (deviceId, Ro1, sensorType1, pin_one),
        (deviceId, Ro2, sensorType2, pin_two),
        (deviceId, Ro3, sensorType3, pin_three),
        ]

    	sql = "INSERT INTO raspberry (date, time, device, ro, sensor, value) VALUES (CURDATE(), CURTIME(), %s, %s, %s, %s)"
    	number_of_rows = cursor.executemany(sql, data)
    	db.commit()
    	db.close()
   	
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("MQ-2 %g, MQ-9 %g, MQ-135 %g" % (pin_one, pin_two, pin_three))
        sys.stdout.flush()
        time.sleep(delay)   

except:
    print("\nAbort by user")
