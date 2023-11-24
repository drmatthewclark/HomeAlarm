#!/usr/bin/python3
#
# poll doorbell.  this will check battery status.
#
import RPi.GPIO as GPIO
from signal import pause
from time import sleep
import time
import functions
from multiprocessing import Process
PIN=11 
DELAY=10
last_time=0 

def doorbell():
    print('doorbell', time.time() )
    functions.text('doorbell rung')


def raw_doorbell(channel):

    global last_time
    state = GPIO.input(PIN)
    now = time.time()
    delay = now - last_time
    last_time = now

    if delay > DELAY:
        doorbell()


def listen():
   GPIO.setmode(GPIO.BOARD)
   GPIO.setup(PIN, GPIO.IN)
   GPIO.add_event_detect(PIN, GPIO.RISING, callback=raw_doorbell)
   pause()


p = Process(target=listen)
p.start()

