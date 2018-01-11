#!/usr/bin/python


import urllib2
import urllib

# This function makes a get request. Use it to do a simple test to see
# if you can reach the api server. If it is successful it will print
# the response from the console
#
def makeGetRequest():

    url = "http://54.244.200.105/readings?gasName=all&startDateTime=weekago&endDateTime=now"

    response = urllib.urlopen(url).read()

    print response

    return ""



# http://54.244.200.105/readings/calculate?
# deviceId=PleaseSendDeviceIdNextTime&instant=now&latitude=33.962492&longitude=-118.437547&sensorType=MQ-2&reading=30

def makePostRequest( sensorType = 'MQ-2',
                     reading = 500,
                     deviceId = 'PleaseSendDeviceIdNextTime',
                     lat = 33.962492,
                     lon = -118.437547
                     ):



    url = 'http://54.244.200.105/readings/calculate?deviceId=' + deviceId + '&instant=now&latitude=' + str(lat) + '&longitude=' + str(lon) + '&sensorType=' + sensorType + '&reading=' + str(reading)

    print "url for POST is: " + url

    #we are not using the query_args now, I'm leaving it here for future
    query_args = {}
    data = urllib.urlencode(query_args)

    request = urllib2.Request(url, data)

    response = urllib2.urlopen(request)

    print "The response code from the server is: ", response.code

    return ""
