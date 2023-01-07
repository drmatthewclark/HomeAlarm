#!/usr/bin/python3
#
# poll doorbell.  this will check battery status.
#
import RPi.GPIO as GPIO
import googlespeak
 
PIN=7 


def doorbell(channel):
    print("doorbell battery low")


def main():
   GPIO.setmode(GPIO.BOARD)
   GPIO.setup(PIN, GPIO.IN)
   GPIO.add_event_detect(PIN, GPIO.BOTH, callback=doorbell)
   state = GPIO.input(PIN)

   if state == 1:
      battery = 'good'
   else:
      battery = 'low'
      googlespeak.announce('doorbell battery is low')

   print('battery is ', battery)


main()
