import socket
from urllib2 import urlopen
import json

local_ip = socket.gethostbyname(socket.gethostname())
print 'Local IP : ' + local_ip + '\n'

public_ip = urlopen('http://ip.42.pl/raw').read()

print 'Public IP : ' + public_ip + '\n'

url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)

public_ip2=data['ip']
#org=data['org']
#city = data['city']
#country=data['country']
#region=data['region']
location=data['loc']
postal=data['postal']

print 'Public IP 2 : ' + public_ip2 + '\n'
print 'Location: ' + location + '\n'
print 'Zip: ' + postal + '\n'
