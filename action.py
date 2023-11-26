"""
This file is part of HomeAlarm.

HomeAlarm is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

HomeAlarm is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <https://www.gnu.org/licenses/>.

Copyright Matthew Clark 2020

"""
import googlespeak as gs
import functions 
import time
from multiprocessing import Process
import logging

volume=90  # normally 100, set lower for testing
silentAlarm = False


#'''
# sound door alert
# use current googleplay volume
#'''
def door_alert(source):
    gs.announce(source)


#'''
# sound fire alarm, log action, send emails
#'''
def fire_alert(source):
   print("*** fire alert: " + source)
   functions.trigger()
   alert = "fire alarm " + source
   functions.smail(alert)
   functions.log_action(alert, "fire")
   logging.warning('FIRE ALERT - ' + source )

   while functions.get_status()["triggered"] and not silentAlarm:
       gs.announce("FIRE " + source  + " FIRE " + source , volume)
       time.sleep(1.0)
       gs.playmp3("fire.mp3", volume)
       time.sleep(1.0)


#'''
# sound the alarm
#''' 
def alarm_alert(source):
   print("*** alarm alert: " + source)
   functions.trigger()
   alert = "alarm " + source
   functions.smail(alert)
   functions.log_action(alert, "alarm")

   logging.warning('ALARM ALERT - ' + source )

   if not silentAlarm:   
   	gs.announce("alarm alarm alarm " + source + " violated  " , volume) 
   	time.sleep(1.0)
   	gs.announce("police dispatch confirmed", volume)

   while functions.get_status()["triggered"] and not silentAlarm:
        gs.announce("alarm" + source + " violated  " , volume) 
        time.sleep(1.0)
        gs.playmp3("sirenhilowithrumbler.wav", volume)
        time.sleep(0.5)

#
# sound water alarm
#
def water_alert(source):
    print("*** water alert: " + source)
    functions.trigger()
    alert = "water " + source
    functions.smail(alert)
    functions.log_action(alert, "water")
    logging.warning('water alert ' + source )

    while functions.get_status()["triggered"]:
        gs.announce("water detected " + source + " water detected", volume)
        time.sleep(1.0)
        gs.announce("water detected " + source + " water detected", volume)
        time.sleep(60)



#
# name - name of device sending signal
# status_result - open/closed/fire etc.
# type - type - door/window/fire/motion/water
#
def action(name, status_result, type):
   #print("action: " + name + "," + status_result + "," + type)
   status = functions.get_status()
   global silentAlarm

   # set silent alarm status 
   if status["silent-alarm"]:
      silentAlarm = True
   else:
      silentAlarm = False

#
# mutually exclusive alarms; only one will be activated
# fire and water alarms always sound independent of other
# settings

   if   type == "fire":                    # fire alaerm
      fire_alert(name)
   elif type == "water":                   # water alarm
      water_alert(name)

   elif status["alarm-stay"] and type in ("door", "window"):  # perimeter
      alarm_alert(name)
   elif status["alarm-away"]:  # all devices will set off alarm
      alarm_alert(name)
   elif status["door alert"] and type in ("door", "window"):
      door_alert(name + " " + status_result)

   return
