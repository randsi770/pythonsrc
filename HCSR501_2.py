#!/usr/bin env python
# -*- coding: utf8 -*-
# Quelle:
# https://www.einplatinencomputer.com/raspberry-pi-pir-bewegungsmelder-ansteuern/
#
#Import
import RPi.GPIO as GPIO
import time
from datetime import datetime
import subprocess
import os
 
print "BEWEGUNGSMELDER"
print ""
 
#Board Mode: Angabe der Pin-Nummer
GPIO.setmode(GPIO.BOARD)
 
#GPIO Pin definieren fuer den Dateneingang vom Sensor
PIR_GPIO = 8
GPIO.setup(PIR_GPIO, GPIO.IN)
 
def MOTION(PIR_GPIO):
    os.system("echo  \"Bewegung erkannt\"")
    time = datetime.now()
    filename = "capture-%04d%02d%02d-%02d%02d%02d.jpg" % (time.year, time.month, time.day, time.hour, time.minute, time.second)
    subprocess.call("raspistill -w 1296 -h 972 -t 1 -e jpg -q 15 -o %s" % filename, shell=True)
    print "Captured %s" % filename
 
print "%s - Warten auf Bewegung" % datetime.now()  
try:
     GPIO.add_event_detect(PIR_GPIO, GPIO.RISING, callback=MOTION)
     while 1:
          time.sleep(60)
except KeyboardInterrupt:
	GPIO.cleanup() 
