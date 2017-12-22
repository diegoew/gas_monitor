import sys
import requests
import datetime
import json


BASE_URI = "http://54.244.200.105/"

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



class WebService:

    def __init__(self, config):
        web_service_config = config("WEB_SERVICE")
        self.BASE_URI = BASE_URI
        self.device_id = web_service_config.get('device_id')
        self.latlng = getUserLatLng();
        self.unit_of_reading = "ppm"


    def getExample(self):
        #r = requests.get("https://httpbin.org/get")
        r = requests.get(self.BASE_URI + "exampleGetValue")

        try:
            r.raise_for_status()
            response = r.json()
            content = response.get('content')
            return content
        except requests.exceptions.RequestException as e:
            print("Webservice error: {0}".format(str(e)))
            sys.exit(1)


    def getReadings(self):
        #r = requests.get("https://httpbin.org/get")
        r = requests.get(self.BASE_URI + "readings")

        try:
            r.raise_for_status()
            response = r.json()
            #content = response.get('content')
            return response
        except requests.exceptions.RequestException as e:
            print("Webservice error: {0}".format(str(e)))
            sys.exit(1)



    def postReading(self, channel_name, reading):
        # server takes iso format
        timestamp = datetime.datetime.now().isoformat()

        # the Webserver requires our JSON to come as an enumerable object
        payload = [{"reading": reading,
                   "gasName": channel_name,
                   "deviceId": self.device_id,
                   "latitude": float(self.latlng[0]),
                   "longitude": float(self.latlng[1]),
                    "unitOfReading": self.unit_of_reading}]

        url = self.BASE_URI + "readings"

        headers = {'content-type': 'application/json'}

        r = requests.post(url= url,
                          data= json.dumps(payload),
                          headers=headers)
        try:
            if r.ok:
                print("{0} data sent successfully!".format(channel_name))
        except requests.exceptions.RequestException as e:
            print("Webservice error: {0}".format(str(e)))
            sys.exit(1)
