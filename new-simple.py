import time
import Adafruit_ADS1x15


# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

# gain for reading voltages from -6.144V to +6.144V.
GAIN = 2/3

print('Reading ADS1115 values, press Ctrl-C to quit...')

# Main loop.
while True:
    # Read all the ADC channel values in a list.
    values = [0]*4
    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        values[i] = adc.read_adc(i, gain=GAIN)
        
    # Print the ADC values.
    print('MQ-9: {0:>6} | MQ-4: {1:>6} | MQ-2: {2:>6} | PM: {3:>6} |'.format(*values))
    
	# Pause for half a second.
    time.sleep(0.5)

