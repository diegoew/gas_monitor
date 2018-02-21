#!/usr/bin/python

import time
import threading


# This is a fuction that returns True if a time interval has not been reached
def didWeReachInterval(startTime, numberOfMinutes):

    elapsed_time = time.time() - startTime

    if elapsed_time > (numberOfMinutes * 60):
        print "wait time reached ", (elapsed_time)
        return False
    else:
        print "time interval ", elapsed_time
        return True


def checkInterval():
    #create a start time
    start = time.time()


    #loop until the interval has been reached
    while didWeReachInterval(start, .25):
        time.sleep(5)

def justPrint():
    print "justPrint is saying printing once, and I'm done!"
    time.sleep(1)


tasks = [justPrint, checkInterval]

for task in tasks:
    t = threading.Thread(target=task)
    t.start()


