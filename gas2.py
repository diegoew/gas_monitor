#from .mq2 import MQ
import time

from .client.config import Config
from .client.webService import WebService
import pprint as pp

def run():

# ======================================
# I kinda canibalized this file, but it
# didn't look like anyone was using it.
# - LOL
# =======================================
    #try:
        print("Press CTRL+C to abort.")

        config = Config()

        web = WebService(config)

        print("\n## Example GET ##")
        print('Web service says: "{0}"\n'.format(web.getExample()))
        print("## POST READINGS ##")
        web.postReading("methane",2.07)
        print("## GET READINGS ##")
        readings = web.getReadings()
        pp.pprint('Last 3 readings: "{0}"\n'.format(readings[-3:]))
        print("Reading Count: {0}".format(len(readings)))

 #       mq2 = MQ();
  #      while True:
   #         perc = mq2.MQPercentage()
    #        sys.stdout.write("\r")
     #       sys.stdout.write("\033[K")
      #      sys.stdout.write("CH1-LPG: %g ppm, CH2-LPG: %g ppm, CH3-LPG: %g ppm" % (perc["GAS_LPG"], perc["GAS_LPG_B"], perc["GAS_LPG_C"]))
       #     sys.stdout.flush()
#
 #           time.sleep(0.1)

    #except:
        print("\nAbort by user")
