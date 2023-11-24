#!/usr/bin/python3
#
# poll doorbell.  this will check battery status.
#
import RPi.GPIO as GPIO
import googlespeak
 
PIN=7 

def main():
   GPIO.setmode(GPIO.BOARD)
   GPIO.setup(PIN, GPIO.IN)
   state = GPIO.input(PIN)

   if state == 1:
      battery = 'good'
   else:
      battery = 'low'
      googlespeak.announce('doorbell battery is low')

   print('battery is', battery)


main()
