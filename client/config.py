import os
import requests

from gas_monitor.client import gasMonitorPath
from configparser import ConfigParser
#create config if none exists

config_file = gasMonitorPath.config('config.ini')


def verifyPath():

    if not os.path.exists(gasMonitorPath.CONFIG_PATH):
        try:
            os.makedirs(gasMonitorPath.CONFIG_PATH)
        except OSError:
            return False

    # make sure we can write to config
    if not os.access(gasMonitorPath.CONFIG_PATH, os.W_OK):
        return False

    return True


def getUserLatLng():
    # we'll use an API for now to get
    r = requests.get("http://freegeoip.net/json/")

    try:

        r.raise_for_status()
        response = r.json()

        latitude = response.get('latitude')
        longitude = response.get('longitude')

        return (latitude, longitude)

    except:
        return (None,None)


class Config:
    def __init__(self):
        self.parser = ConfigParser()
        self.populateDefaults()
        self.data = self.getConfig()


    def __call__(self,sectionKey ,*args, **kwargs):
        return self.data[sectionKey]


    def getConfig(self):
        parsed = None

        if not verifyPath():
            raise

        # try to read config file
        try:
            parser = ConfigParser()
            parsed = parser.read(config_file)

        except OSError:
            raise

        if parser == None:
            return {}

        sections = parser.sections()

        config_data = {}

        for section in parser.sections():
            config_data[section] = {}
            if len(parser[section]) ==0:
                continue
            for key in parser[section]:
                config_data[section][key] = parser[section][key]

        return config_data




    def populateDefaults(self):

        def simpleRequest(keyword, printedName, setAsType=None):
            user_input = input(printedName + " : ")
            if user_input:
                if setAsType:
                    user_input = setAsType(user_input)
            return (keyword, user_input)

        if 'WEB_SERVICE' not in self.parser:
            self.parser['WEB_SERVICE'] = {}

        webService = self.parser['WEB_SERVICE']


        ## Web Service ##
        web_key, web_value = simpleRequest('device_id', 'Please provide your Device ID?', str)

        webService[web_key] = web_value

        latitude, longitude = getUserLatLng()

        webService["latitude"] = str(latitude)
        webService["longitude"] = str(longitude)

        ## Write user imputs to file ##
        with open(config_file, 'w') as file:
            self.parser.write(file)
        file.close()