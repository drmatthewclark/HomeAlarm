
import googlespeak as gs
import functions 
import time
from multiprocessing import Process


volume=10  # normally 100, set lower for testing
silentAlarm = False


#'''
# sound door alert
# use current googleplay volume
#'''
def door_alert(source):
    gs.announce(source, None)


#'''
# sound fire alarm, log action, send emails
#'''
def fire_alert(source):
   print("*** fire alert: " + source)
   functions.trigger()
   alert = "fire alarm " + source
   functions.smail(alert)
   functions.log_action(alert, "fire")
   while functions.get_status()["triggered"] and not silentAlarm:
       gs.announce("FIRE " + source  + " FIRE " + source , volume)
       time.sleep(1.0)
       gs.playmp3("/5920ddcqeag/fire.mp3", volume)
       time.sleep(1.0)


#'''
# sound the alarm
#''' 
def alarm_alert(source):
   print("*** alarm alert: " + source)
   print(str(status)) 
   functions.trigger()
   alert = "alarm " + source
   functions.smail(alert)
   functions.log_action(alert, "alarm")
   gs.announce("alarm alarm alarm " + source + " violated  " , volume) 
   time.sleep(1.0)
   gs.announce("police dispatch confirmed", volume)
   while functions.get_status()["triggered"] and not silentAlarm:
        gs.announce("alarm" + source + " violated  " , volume) 
        time.sleep(1.0)
        gs.playmp3("/5920ddcqeag/sirenhilowithrumbler.wav", volume)
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
   print("action: " + name + "," + status_result + "," + type)
   status = functions.get_status()

   # set silent alarm status 
   if status["silent-alarm"]:
      silentAlarm = True
   else:
      silentAlarm = False

#
# mutually exclusive alarms; only one will be activated
#
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

#
# start a function in a thread
#
def startThread(funcname, args):
      Process(target = funcname, args=args).start()


# test
#action("front door", "open", "door")  
#print(functions.get_status()["triggered"] )
 
