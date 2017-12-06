# adapted from:
# http://sandboxelectronics.com/?p=165
# https://tutorials-raspberrypi.com/configure-and-read-out-the-raspberry-pi-gas-sensor-mq-x/
# https://github.com/mdsiraj1992/Gassensors

import time
import math
from MCP3008 import MCP3008

class MQ():

    ######################### Hardware Related Macros #########################
    MQ2_PIN                      = 0        # define which analog input channel you are going to use for the MQ-2 sensor (MCP3008)
    MQ9_PIN                      = 1        # define which analog input channel you are going to use for the MQ-5 sensor (MCP3008)
    MQ135_PIN                    = 2        # define which analog input channel you are going to use for the MQ-135 sensor (MCP3008)    

    RL_VALUE_MQ2                 = 1        # define the load resistance on the board, in kilo ohms
    RO_CLEAN_AIR_FACTOR_MQ2      = 9.58     # RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO,
                                            # which is derived from https://github.com/mdsiraj1992/Gassensors
    RL_VALUE_MQ9                 = 18       # define the load resistance on the board, in kilo ohms
    RO_CLEAN_AIR_FACTOR_MQ2      = 9.8      # RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO,
                                            # which is derived from https://github.com/mdsiraj1992/Gassensors
    RL_VALUE_MQ135               = 19       # define the load resistance on the board, in kilo ohms
    RO_CLEAN_AIR_FACTOR_MQ2      = 3.59     # RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO,
                                            # which is derived from https://github.com/mdsiraj1992/Gassensors

                                           
 
    ######################### Software Related Macros #########################
    CALIBARAION_SAMPLE_TIMES     = 50       # define how many samples you are going to take in the calibration phase
    CALIBRATION_SAMPLE_INTERVAL  = 500      # define the time interal(in milisecond) between each samples in the
                                            # cablibration phase
    READ_SAMPLE_INTERVAL         = 50       # define how many samples you are going to take in normal operation
    READ_SAMPLE_TIMES            = 5        # define the time interal(in milisecond) between each samples in 
                                            # normal operation
 
    ######################### Application Related Macros ######################

    # MQ-2: They are used in gas leakage detecting equipments in family and industry, are suitable for detecting of
    # LPG, i-butane, propane, methane, alcohol, hydrogen, smoke.
    MQ2_GAS_LPG                  = 0
    MQ2_GAS_CO                   = 1
    MQ2_GAS_SMOKE                = 2
    MQ2_GAS_HYDROGEN             = 3  # H2
    MQ2_GAS_METHANE              = 4  # CH4
    MQ2_GAS_ALCOHOL              = 5
    MQ2_GAS_PROPANE              = 6  # C3H8

    # MQ-9: MQ-9 gas sensor has high sensitity to Carbon Monoxide, Methane and LPG. The sensor could be used to detect
    # different gases contains CO and combustible gases, it is with low cost and suitable for different application.
    MQ9_GAS_LPG                  = 7
    MQ9_GAS_CO                   = 8
    MQ9_GAS_METHANE              = 9   # CH4

    # MQ-135: They are used in air quality control equipments for buildings/offices, are suitable for detecting
    # of NH3, NOx, alcohol, benzene, CO2 and smoke. 
    MQ135_GAS_CO2                = 10
    MQ135_GAS_CO                 = 11
    MQ135_GAS_ALCOHOL            = 12
    MQ135_GAS_AMMONIUM           = 13   # NH4
    MQ135_GAS_TOLUENE            = 14   # CH3
    MQ135_GAS_ACETONE            = 15   # (CH3)2CO
  
    

    def __init__(self, Ro=10, analogPin=0):
        self.Ro = Ro
        self.MQ2_PIN = 0
        self.MQ9_PIN = 1
        self.MQ135_PIN = 3       
        self.adc = MCP3008()

        # MQ-2        
        self.MQ2LPGCurve = [2.3,0.23,-0.48]      # two points are taken from the curve. 
                                                 # with these two points, a line is formed which is "approximately equivalent"
                                                 # to the original curve. 
                                                 # data format:{ x, y, slope}; point1: (lg200, 0.23), point2: (lg10000, -0.59) 
        self.MQ2COCurve = [2.3,0.71,-0.32]       # two points are taken from the curve. 
                                                 # with these two points, a line is formed which is "approximately equivalent" 
                                                 # to the original curve.
                                                 # data format:[ x, y, slope]; point1: (lg200, 0.71), point2: (lg10000,  0.17)
        self.MQ2SmokeCurve =[2.3,0.54,-0.45]     # two points are taken from the curve. 
                                                 # with these two points, a line is formed which is "approximately equivalent" 
                                                 # to the original curve.
                                                 # data format:[ x, y, slope]; point1: (lg200, 0.54), point2: (lg10000,  -0.22)  
        self.MQ2HydrogenCurve =[2.3,0.32,-0.47]  # two points are taken from the curve. 
                                                 # with these two points, a line is formed which is "approximately equivalent" 
                                                 # to the original curve.
                                                 # data format:[ x, y, slope]; point1: (lg200, 0.32), point2: (lg10000,  -0.48) 
        self.MQ2MethaneCurve =[2.3,0.50,-0.40]   # two points are taken from the curve. 
                                                 # with these two points, a line is formed which is "approximately equivalent" 
                                                 # to the original curve.
                                                 # data format:[ x, y, slope]; point1: (lg200, 0.50), point2: (lg10000,  -0.17) 
        self.MQ2AlcoholCurve =[2.3,0.46,-0.38]   # two points are taken from the curve. 
                                                 # with these two points, a line is formed which is "approximately equivalent" 
                                                 # to the original curve.
                                                 # data format:[ x, y, slope]; point1: (lg200, 0.46), point2: (lg10000,  -0.19) 
        self.MQ2PropaneCurve =[2.3,0.25,-0.47]   # two points are taken from the curve. 
                                                 # with these two points, a line is formed which is "approximately equivalent" 
                                                 # to the original curve.
                                                 # data format:[ x, y, slope]; point1: (lg200, 0.25), point2: (lg10000,  -0.55)

        # MQ-9 
        self.MQ9LPGCurve = [2.3,0.23,-0.48]      # two points are taken from the curve. 
                                                 # with these two points, a line is formed which is "approximately equivalent"
                                                 # to the original curve. 
                                                 # data format:{ x, y, slope}; point1: (lg200, 0.23), point2: (lg10000, -0.59) 
        self.MQ9COCurve = [2.3,0.71,-0.32]       # two points are taken from the curve. 
                                                 # with these two points, a line is formed which is "approximately equivalent" 
                                                 # to the original curve.
                                                 # data format:[ x, y, slope]; point1: (lg200, 0.71), point2: (lg10000,  0.17)
        self.MQ9MethaneCurve =[2.3,0.50,-0.40]   # two points are taken from the curve. 
                                                 # with these two points, a line is formed which is "approximately equivalent" 
                                                 # to the original curve.
                                                 # data format:[ x, y, slope]; point1: (lg200, 0.50), point2: (lg10000,  -0.17)

        # MQ-135 
        self.MQ135CO2Curve = [2.3,0.23,-0.48]    # two points are taken from the curve. 
                                                 # with these two points, a line is formed which is "approximately equivalent"
                                                 # to the original curve. 
                                                 # data format:{ x, y, slope}; point1: (lg200, 0.23), point2: (lg10000, -0.59) 
        self.MQ135COCurve = [2.3,0.71,-0.32]     # two points are taken from the curve. 
                                                 # with these two points, a line is formed which is "approximately equivalent" 
                                                 # to the original curve.
                                                 # data format:[ x, y, slope]; point1: (lg200, 0.71), point2: (lg10000,  0.17)
        self.MQ135AlcoholCurve =[2.3,0.46,-0.38] # two points are taken from the curve. 
                                                 # with these two points, a line is formed which is "approximately equivalent" 
                                                 # to the original curve.
                                                 # data format:[ x, y, slope]; point1: (lg200, 0.46), point2: (lg10000,  -0.19)
        self.MQ135AmmoniumCurve =[2.3,0.46,-0.38] # two points are taken from the curve. 
                                                 # with these two points, a line is formed which is "approximately equivalent" 
                                                 # to the original curve.
                                                 # data format:[ x, y, slope]; point1: (lg200, 0.46), point2: (lg10000,  -0.19) 
        self.MQ135TolueneCurve =[2.3,0.46,-0.38] # two points are taken from the curve. 
                                                 # with these two points, a line is formed which is "approximately equivalent" 
                                                 # to the original curve.
                                                 # data format:[ x, y, slope]; point1: (lg200, 0.46), point2: (lg10000,  -0.19)
        self.MQ135AcetoneCurve =[2.3,0.46,-0.38] # two points are taken from the curve. 
                                                 # with these two points, a line is formed which is "approximately equivalent" 
                                                 # to the original curve.
                                                 # data format:[ x, y, slope]; point1: (lg200, 0.46), point2: (lg10000,  -0.19)

                
        print("Calibrating MQ-2...")
        self.Ro = self.MQCalibration(self.MQ2_PIN)
        print("Calibration is done...\n")
        print("Ro=%f kohm" % self.Ro)

        print("Calibrating MQ-9...")
        self.Ro = self.MQCalibration(self.MQ9_PIN)
        print("Calibration is done...\n")
        print("Ro=%f kohm" % self.Ro)

        print("Calibrating MQ-135...")
        self.Ro = self.MQCalibration(self.MQ135_PIN)
        print("Calibration is done...\n")
        print("Ro=%f kohm" % self.Ro)

    
    
    def MQPercentage(self):
        val = {}

        read = self.MQRead(self.MQ2_PIN)
        val["MQ2_LPG"]      = self.MQGetGasPercentage(read/self.Ro, self.MQ2_GAS_LPG)
        val["MQ2_CO"]       = self.MQGetGasPercentage(read/self.Ro, self.MQ2_GAS_CO)
        val["MQ2_SMOKE"]    = self.MQGetGasPercentage(read/self.Ro, self.MQ2_GAS_SMOKE)
        val["MQ2_HYDROGEN"] = self.MQGetGasPercentage(read/self.Ro, self.MQ2_GAS_HYDROGEN)		
        val["MQ2_METHANE"]  = self.MQGetGasPercentage(read/self.Ro, self.MQ2_GAS_METHANE)		
        val["MQ2_ALCOHOL"]  = self.MQGetGasPercentage(read/self.Ro, self.MQ2_GAS_ALCOHOL)	
        val["MQ2_PROPANE"]  = self.MQGetGasPercentage(read/self.Ro, self.MQ2_GAS_PROPANE)	

        read = self.MQRead(self.MQ2_PIN)
        val["MQ9_LPG"]      = self.MQGetGasPercentage(read/self.Ro, self.MQ9_GAS_LPG)
        val["MQ9_CO"]       = self.MQGetGasPercentage(read/self.Ro, self.MQ9_GAS_CO)
        val["MQ9_METHANE"]  = self.MQGetGasPercentage(read/self.Ro, self.MQ9_GAS_METHANE)		

        read = self.MQRead(self.MQ2_PIN)
        val["MQ135_CO2"]      = self.MQGetGasPercentage(read/self.Ro, self.MQ135_GAS_CO2)
        val["MQ135_CO"]       = self.MQGetGasPercentage(read/self.Ro, self.MQ135_GAS_CO)	
        val["MQ135_ALCOHOL"]  = self.MQGetGasPercentage(read/self.Ro, self.MQ135_GAS_ALCOHOL)	
        val["MQ135_AMMONIUM"] = self.MQGetGasPercentage(read/self.Ro, self.MQ135_GAS_AMMONIUM)
        val["MQ135_TOLUENE"]  = self.MQGetGasPercentage(read/self.Ro, self.MQ135_GAS_TOLUENE)
        val["MQ135_ACETONE"]  = self.MQGetGasPercentage(read/self.Ro, self.MQ135_GAS_ACETONE)
        
        return val
        
    ######################### MQResistanceCalculation #########################
    # Input:   raw_adc - raw value read from adc, which represents the voltage
    # Output:  the calculated sensor resistance
    # Remarks: The sensor and the load resistor forms a voltage divider. Given the voltage
    #          across the load resistor and its resistance, the resistance of the sensor
    #          could be derived.
    ############################################################################ 
    def MQResistanceCalculation(self, raw_adc):
        return float(self.RL_VALUE*(1023.0-raw_adc)/float(raw_adc));
     
     
    ######################### MQCalibration ####################################
    # Input:   mq_pin - analog channel
    # Output:  Ro of the sensor
    # Remarks: This function assumes that the sensor is in clean air. It use  
    #          MQResistanceCalculation to calculates the sensor resistance in clean air 
    #          and then divides it with RO_CLEAN_AIR_FACTOR. RO_CLEAN_AIR_FACTOR is about 
    #          10, which differs slightly between different sensors.
    ############################################################################ 
    def MQCalibration(self, mq_pin):
        val = 0.0
        for i in range(self.CALIBARAION_SAMPLE_TIMES):          # take multiple samples
            val += self.MQResistanceCalculation(self.adc.read(mq_pin))
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL/1000.0)
            
        val = val/self.CALIBARAION_SAMPLE_TIMES                 # calculate the average value

        val = val/self.RO_CLEAN_AIR_FACTOR                      # divided by RO_CLEAN_AIR_FACTOR yields the Ro 
                                                                # according to the chart in the datasheet 

        return val;
      
      
    #########################  MQRead ##########################################
    # Input:   mq_pin - analog channel
    # Output:  Rs of the sensor
    # Remarks: This function use MQResistanceCalculation to caculate the sensor resistenc (Rs).
    #          The Rs changes as the sensor is in the different consentration of the target
    #          gas. The sample times and the time interval between samples could be configured
    #          by changing the definition of the macros.
    ############################################################################ 
    def MQRead(self, mq_pin):
        rs = 0.0

        for i in range(self.READ_SAMPLE_TIMES):
            rs += self.MQResistanceCalculation(self.adc.read(mq_pin))
            time.sleep(self.READ_SAMPLE_INTERVAL/1000.0)

        rs = rs/self.READ_SAMPLE_TIMES

        return rs
     
    #########################  MQGetGasPercentage ##############################
    # Input:   rs_ro_ratio - Rs divided by Ro
    #          gas_id      - target gas type
    # Output:  ppm of the target gas
    # Remarks: This function passes different curves to the MQGetPercentage function which 
    #          calculates the ppm (parts per million) of the target gas.
    ############################################################################ 
    def MQGetGasPercentage(self, rs_ro_ratio, gas_id):
        if ( gas_id == self.GAS_LPG ):
            return self.MQGetPercentage(rs_ro_ratio, self.LPGCurve)
        elif ( gas_id == self.GAS_CO ):
            return self.MQGetPercentage(rs_ro_ratio, self.COCurve)
        elif ( gas_id == self.GAS_SMOKE ):
            return self.MQGetPercentage(rs_ro_ratio, self.SmokeCurve)
        elif ( gas_id == self.GAS_HYDROGEN ):
            return self.MQGetPercentage(rs_ro_ratio, self.HydrogenCurve)
        elif ( gas_id == self.GAS_METHANE ):
            return self.MQGetPercentage(rs_ro_ratio, self.MethaneCurve)
        elif ( gas_id == self.GAS_ALCOHOL ):
            return self.MQGetPercentage(rs_ro_ratio, self.AlcoholCurve)
        elif ( gas_id == self.GAS_PROPANE ):
            return self.MQGetPercentage(rs_ro_ratio, self.PropaneCurve)
        return 0
     
    #########################  MQGetPercentage #################################
    # Input:   rs_ro_ratio - Rs divided by Ro
    #          pcurve      - pointer to the curve of the target gas
    # Output:  ppm of the target gas
    # Remarks: By using the slope and a point of the line. The x(logarithmic value of ppm) 
    #          of the line could be derived if y(rs_ro_ratio) is provided. As it is a 
    #          logarithmic coordinate, power of 10 is used to convert the result to non-logarithmic 
    #          value.
    ############################################################################ 
    def MQGetPercentage(self, rs_ro_ratio, pcurve):
        return (math.pow(10,( ((math.log(rs_ro_ratio)-pcurve[1])/ pcurve[2]) + pcurve[0])))

