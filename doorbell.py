#!/usr/bin/python3
#
# poll doorbell.  this will check battery status.
#
import RPi.GPIO as GPIO
from signal import pause
from time import sleep
import logging

import time
import datetime
import functions
from multiprocessing import Process

PIN = 11  # gpio pi
BOUNCETIME = 5000  # bouncetime betwween events, millliseconds
DELAY = 30  # only trigger  this often, seconds
last_time = 0  # last event time

pid = None


def doorbell():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S' )
    print('doorbell', now) 
    logging.info('doorbell rung')
    functions.smail(f'doorbell rung at {now}')


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
    GPIO.add_event_detect(
        PIN, GPIO.RISING, callback=raw_doorbell, bouncetime=BOUNCETIME)
    pause()


def start():
    logging.info('started doorbell listener')
    pid = Process(name='doorbell', target=listen)
    pid.start()


def stop():
    logging.info('stopping doorbell listener')
    pid.terminate()
