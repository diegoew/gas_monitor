from mq import *
import sys, time

try:
    print("Press CTRL+C to abort.")
    
    mq = MQ();
    while True:
        perc = mq.MQPercentage()
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm, H2: %g ppm, CH4: %g ppm, Alcohol: %g ppm, Propane: %g ppm" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"], perc["HYDROGEN"], perc["METHANE"], perc["ALCOHOL"], perc["PROPANE"]))
        sys.stdout.flush()
        time.sleep(0.1)

except:
    print("\nAbort by user")