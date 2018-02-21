#!/usr/bin/python

import time

# This is a fuction that returns True if a time interval has not been reached
def didWeReachInterval(startTime, numberOfMinutes):

    elapsed_time = time.time() - startTime

    if elapsed_time > (numberOfMinutes * 60):
        print "wait time reached ", (elapsed_time)
        return False
    else:
        print "time interval ", elapsed_time
        return True


# This is a fuction shows us how to use function didWeReachInterval
def checkInterval():
    #create a start time
    start = time.time()


    #loop until the interval has been reached
    while didWeReachInterval(start, .25):
        time.sleep(5)


# Run the program
checkInterval()


