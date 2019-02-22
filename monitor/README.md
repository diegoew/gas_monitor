### Requirements:
- MQ series sensors
- ADS1115 analog-to-digital converter (ADC) - https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/ads1015-slash-ads1115
- Raspberry Pi
- Python program running on Raspberry Pi

### Monitor software

`monitor.py`
- Optinally calibrates the sensors (calculates Ro values)
  * Averages 50 samples in "clean air" to calculate RO for each sensor 
- Periodically reads sensor data from the ADC
- Logs events and data to a file
- Stores readings to a local database
- Uploads data to a server to be aggregated and displayed on the website

### Installation

1. Connect the Raspberry Pi:
    - a micro-USB 5V power to port 1 
    - a micro-USB keyboard to port 2
    - a display device via micro-HDMI to micro-HTDMI port
1. Connect the Raspberry Pi to the Internet
1. Log into the Raspberry Pi and open a terminal
1. Execute<br>`git clone https://github.com/diegoew/gas_monitor.git && cd gas_monitor/monitor && sudo pip3 install -r requirements.txt`
1. Edit file `config.py` items `DEVICE_ID`, `LAT`, `LON`, `ADC_TYPE`, 
`SENSOR_TYPES` and `OPENWEATHER_KEY`
1. Execute<br>`sudo systemctl daemon-reload && sudo systemctl enable --now $PWD/gas-monitor.service`
1. Check the [server graph](http://www.protectplayanow.org/gas-monitor-testpage.html)

### Control and logs
1. To stop the service: `sudo systemctl stop gas-monitor`
1. To start the service:`sudo systemctl start gas-monitor`
1. To check the status: `systemctl status gas-monitor`
1. To see the log: `journalctl -u gas-monitor.service` and 
`tail -f /var/log/messages`
1. To see the database of readings: `sqlite3 readings.sqlite`
