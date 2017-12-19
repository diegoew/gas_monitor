import requests


class WebService:

    def __init__(self, config):
        web_service_config = config("WEB_SERVICE")
        self.BASE_URI = web_service_config['base_uri']


    def getTempExample(self):
        r = requests.get("https://httpbin.org/get")
        #r = requests.get(self.BASE_URI + "exampleGetValue")

        try:
            r.raise_for_status()
            response = r.json()
            origin = response.get('origin')
            return "Successfully made Http GET call from {0}!".format(origin)
        except:
            print("WebService unable to get example!")