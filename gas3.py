from mq-2 import *
from mq-9 import *
from mq-135 import *
import sys, time

try:
    print("Press CTRL+C to abort.")
    
    mq-2 = MQ();
    mq-9 = MQ();
    mq-135 = MQ();
    while True:
        perc_mq2 = mq-2.MQPercentage()
        perc_mq9 = mq-9.MQPercentage()
        perc_mq135= mq-135.MQPercentage()
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("CH1-LPG: %g ppm, CH2-LPG: %g ppm, CH3-LPG: %g ppm" % (perc_mq2["GAS_LPG"], perc_mq9["GAS_LPG"], perc_mq135["GAS_LPG"]))
        sys.stdout.flush()
        time.sleep(0.1)

except:
    print("\nAbort by user")
