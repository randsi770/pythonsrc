#!/usr/bin/env python
# -*- coding: utf8 -*-
import RPi.GPIO as GPIO
import time
import sys, os
import termios, fcntl
import random
from decimal import *

def pause(ms):
	l = Decimal(ms)/Decimal(1000)
	time.sleep(Decimal(ms)/Decimal(1000))
	

def blinke(led,led2,tim):
	GPIO.output(led,1)
	pause(tim)
	GPIO.output(led,0)
	GPIO.output(led2,1)
	pause(tim)
	GPIO.output(led2,0)

fd = sys.stdin.fileno()
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = 17
led2 = 22
GPIO.setup(led,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)

tim = 15
try:
	print("Zum Beenden 'x' drücken")
	while 1:
		try:
			blinke(led,led2,tim)
			tim+=10
			tim = random.randrange(15,1000,1)
			tastatur = sys.stdin.read(1)
			if tastatur == 'x':
				break
		except IOError: pass
finally:
	termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

print("Programm beendet")
GPIO.cleanup()


