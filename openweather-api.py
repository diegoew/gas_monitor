import urllib2
import json

weather_url = 'http://api.openweathermap.org/data/2.5/weather?'
api_key = '177f943c86860b2efb332b00962ac509'    #Unique key, we will need to use one per Gas Monitor. we can read it 60 times per minute.
                                                #This should go to the config file
unit = 'metric'     # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
latitude = '34.0372384'     #This will change by device location, this shoudl also be in the config file                        
logitude = '-118.4260817'   #This will change by device location, this shoudl also be in the config file                       

full_api_url = weather_url + 'lat=' + latitude + '&lon=' + logitude + '&mode=json&units=' + unit + '&appid=' + api_key

f = urllib2.urlopen(full_api_url)

json_string = f.read()
parsed_json = json.loads(json_string)

deg_c = parsed_json['main']['temp']
rel_humidity = parsed_json['main']['humidity']

print "Current temperature: %s; relative humidity: %s" % (deg_c, rel_humidity)
f.close()
