#
# poll doorbell.  this will check battery status.
#
import RPi.GPIO as GPIO
import time
import googlespeak
 
PIN=7 


def doorbell(channel):
    print("doorbell battery low")


def main():
   GPIO.setmode(GPIO.BOARD)
   GPIO.setup(PIN, GPIO.IN)
   GPIO.add_event_detect(PIN, GPIO.BOTH, callback=doorbell)

   state = GPIO.input(PIN)
   print("GPIO state is " + str(state))

   while True:
        time.sleep(3600)

main()
