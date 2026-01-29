#!/usr/bin/python3
#
# poll doorbell.  this will check battery status.
#
import os
import RPi.GPIO as GPIO
from signal import pause
from time import sleep
import googlespeak as gs

import time
import datetime
import functions
from multiprocessing import Process
from logsetup import logsetup

logger = logsetup('doorbell')

PIN = 11  # gpio pi
BOUNCETIME = 10000  # bouncetime betwween events, millliseconds
DELAY = 45  # only trigger  this often, seconds
BELL='bell.wav'
last_time = 0  # last event time

pid = None


def doorbell():
    fname = '/home/pi/frontor.png' 
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S' )
    print('doorbell', now) 
    logger.info('doorbell rung')
    os.system('/home/pi/get_image.sh >/dev/null')
    gs.playmp3(BELL)
    functions.smail(f'doorbell rung at {now}', fname )

def raw_doorbell(channel):

    global last_time
    now = time.time()
    delay = now - last_time
    last_time = now

    if delay > DELAY:
        doorbell()


def listen():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
    GPIO.add_event_detect(
        PIN, GPIO.RISING, callback=raw_doorbell, bouncetime=BOUNCETIME)
    pause()


def start():
    logger.info('started doorbell listener')
    pid = Process(name='doorbell', target=listen)
    pid.start()


def stop():
    logger.info('stopping doorbell listener')
    pid.terminate()
 
if __name__ == '__main__':
   doorbell()
