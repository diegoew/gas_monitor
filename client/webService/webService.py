import requests
import datetime

BASE_URI = "http://54.244.200.105/"

class WebService:

    def __init__(self, config):
        web_service_config = config("WEB_SERVICE")
        self.BASE_URI = BASE_URI
        self.device_id = web_service_config.get('device_id')
        self.longitude = web_service_config.get('longitude')
        self.latitude = web_service_config.get('latitude')

        self.unit_of_measure = "ppm"


    def getExample(self):
        #r = requests.get("https://httpbin.org/get")
        r = requests.get(self.BASE_URI + "exampleGetValue")

        try:
            r.raise_for_status()
            response = r.json()
            content = response.get('content')
            return content
        except:
            print("WebService unable to get example!")


    def getReadings(self):
        #r = requests.get("https://httpbin.org/get")
        r = requests.get(self.BASE_URI + "readings")

        try:
            r.raise_for_status()
            response = r.json()
            content = response.get('content')
            return content
        except:
            print("WebService unable to get readings!")



    def postReading(self, gas_name, reading):
        # server takes iso format
        timestamp = datetime.datetime.now().isoformat()
        payload = {'reading': reading,
                   'gasName': gas_name,
                   'deviceId': self.device_id,
                   'latitude': float(self.latitude),
                   'longitude': float(self.longitude)}
        print('payload: ', str(payload))

        url = self.BASE_URI + "readings"
        print("post Url: ", url)

        headers = {'content-type': 'application/json'}

        r = requests.post(url= url,
                          data=payload,
                          headers=headers)
        #try:
        r.raise_for_status()
        #    print(str(r.json()))
        #except:
        #    print("Webservice unable to post reading!")
