# gas_monitor

### Goal
Better understand fluctuations in air pollutants arising from natural gas operations:
- Natural gas* (a mix of gases)
- Methane (the main component of natural gas ~ 80%–95%)
- CO2 (combustion output of burning natural gas)
- CO (combustion output of burning natural gas with insufficient oxygen)
- NOx (combustion by-product output of burning natural gas)
- Ammonia (used for emission control to reduce NOx)
- Formaldehyde

### Requirements

The basic setup of this air gas monitor consist of: 
- MQ series sensors
- ADS1115 analog-to-digital converter (ADC) - https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/ads1015-slash-ads1115
- Raspberry Pi
- Python program (this code) running on Raspberry Pi
- Website to receive and display measurements
- Cloud sharing program

While the sensors react very fast, they are not exclusively sensitive to just 
one type of gas. Therefore, readings might be skewed by other gases. 

### Monitor software

`monitor.py`
- Optinally calibrates the sensors (calculates Ro values)
  * Averages 50 samples in "clean air" to calculate RO for each sensor 
- Periodically reads sensor data from the ADC
- Displays the readings to standard output
- Logs events and data to a file
- Stores readings to a local database
- Sends data to a server to be aggregated and displayed on the website

### Installation

1. Connect the Raspberry Pi:
    - a micro-USB 5V power to port 1 
    - a micro-USB keyboard to port 2
    - a display device via micro-HDMI to micro-HTDMI port
1. Connect the Raspberry Pi to the Internet
1. Log into the Raspberry Pi and open a terminal
1. Execute<br>`git clone https://github.com/diegoew/gas_monitor.git && cd gas_monitor && sudo pip3 install -r requirements.txt`
1. Edit file `config.py`, at least `DEVICE_ID`, `LAT`, `LON`, `ADC_TYPE`, 
`SENSOR_TYPES` and `OPENWEATHER_KEY`
1. Execute<br>`sudo systemd enable --now $PWD/gas-monitor.service`
1. Check the service log: `journalctl -u gas-monitor.service` and 
standard output: `tail -f /var/log/messages`. 

### More info

Natural gas is a fossil fuel composed almost entirely of methane, but also contains other hydrocarbon gases, including ethane, propane, butane and pentane. It also commonly includes varying amounts of other higher alkanes, and sometimes a small percentage of carbon dioxide, nitrogen, hydrogen sulfide, or helium. Natural gas that is derived from shale gas could include other chemical used in the extraction process of the gas. If mixed with biogas or landfill gas, it can also contain acids and other corrosive substances.

In order to assist in detecting leaks, an odorizer is added to the otherwise colorless and almost odorless natural gas. The odor has been compared to the smell of rotten eggs, due to the added tert-Butylthiol (t-butyl mercaptan). Sometimes, a related compound, thiophane, may be used in the mixture. These additives are also a deferent for humans to inhale the gas. The additives themselves are irritants that can cause nausea in humans, and have more severe health effects with prolonged exposure to the skin, eyes, kidneys, lungs and liver.

Natural gas extraction also produces radioactive isotopes of polonium (Po-210), lead (Pb-210) and radon (Rn-220). Radon is a gas with initial activity from 5 to 200,000 becquerels per cubic meter of gas. It decays rapidly to Pb-210 which can build up as a thin film in gas extraction equipment.

[Project notes](https://docs.google.com/document/d/1aLgA85S5O9_SXOJqAhFqrD8NQ2f40Iqx_LMBxXcsqhk)

[Formulas to convert raw data into ppm gas readings](https://docs.google.com/spreadsheets/d/1bb9lcmV_HsYXKDZiz5pghnakAcYF63pO5d78DDjXMT4/edit?usp=sharing)

[Components for the gas sensor device](https://docs.google.com/spreadsheets/d/18XvdZh5N7-iELkv8ZHe7yIzBQmGSkL3IdELiQ5KsU-c/edit?usp=sharing)

https://www.gofundme.com/gas-monitor-project

https://raspberry-gas-monitor.weebly.com/

http://www.protectplayanow.org/
