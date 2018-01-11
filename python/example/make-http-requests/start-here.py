#!/usr/bin/python

"""
    This is the code that has an example of making a POST http request.

"""

from httpRequests import makeGetRequest
from httpRequests import makePostRequest


# This should print the response from the server
#makeGetRequest()


# This is an example of making a post request that sends data to the server using default values
makePostRequest()


# This is an example of making a post request that sends reading and sensorType
makePostRequest(    reading = 500,
                    sensorType = "MQ-9" )
