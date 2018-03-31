import urllib2
import json
f = urllib2.urlopen('http://api.wunderground.com/api/f4a2a30b572e293e/geolookup/conditions/q/pws:KCALOSAN161.json')
json_string = f.read()
parsed_json = json.loads(json_string)
location = parsed_json['location']['city']
temp_f = parsed_json['current_observation']['temp_f']
wind_dir = parsed_json['current_observation']['wind_dir']
wind_mph = parsed_json['current_observation']['wind_mph']
print "Current temperature in %s is: %s, Wind direction: %s with %s mph" % (location, temp_f, wind_dir, wind_mph)
f.close()
