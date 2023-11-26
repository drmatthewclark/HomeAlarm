#!/usr/bin/python3
#
# poll doorbell.  this will check battery status.
#
import RPi.GPIO as GPIO
import googlespeak
import logging
logging.basicConfig(level=logging.INFO)

mesg = 'doorbell battery is %s'
 
PIN=7 

def main():
   GPIO.setmode(GPIO.BOARD)
   GPIO.setup(PIN, GPIO.IN)
   state = GPIO.input(PIN)

   if state == 1:
      battery = 'good'
      logging.info( mesg % ( battery,) )   
   else:
      battery = 'low'
      googlespeak.announce( mesg % (battery,) )
      logging.warn( mesg % (battery,) )   


main()
