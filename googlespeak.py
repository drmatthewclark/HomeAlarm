#!/usr/bin/python3
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
import sys
import pychromecast
import os
import os.path
import time
import hashlib
from   multiprocessing import Process
import datetime
import socket
import functions
import random
# 
# addresses of google home devices
#broadcast_addresses = {"192.168.20.11", "192.168.20.97" , "192.168.20.18", "192.168.20.20"}
#broadcast_addresses = {"192.168.20.97" } # basement
#
broadcast_addresses = functions.getGoogleHome()

mp3dir="/5920ddcqeag/"    # system-dependent directory to cache sound files
useGoogleHome = True
usePiSpeaker  = True
local_ip = None

def getMyIP():
    testIP = "8.8.8.8"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((testIP, 0))
    ipaddr = s.getsockname()[0]
    return ipaddr

#-----------------------------------------
# create the mp3 file for the text to say
#-----------------------------------------
def makefile(say):
   say = say.replace("_", " ")  # replace underscores

   tmppath= "/var/www/html" 
   fname= mp3dir + hashlib.md5(say.encode()).hexdigest()+".wav"; #create md5 filename for caching
   lfname = tmppath + fname

   if not os.path.isfile(lfname) or os.path.getsize(lfname) == 0:
      cmd = '/usr/bin/pico2wave -w ' + lfname + ' "' + say + '"'
      os.system(cmd)

      fsize = os.path.getsize(lfname)
      if fsize == 0:
          fname = None

   return fname

#-------------------------------------
# say the words on google home
#-------------------------------------
def speak(ip, fname, volume):

   global local_ip
   if local_ip is None:
      local_ip = getMyIP()

   castdevice = pychromecast.Chromecast(ip)
   castdevice.wait()
   vol_previous=castdevice.status.volume_level

   #castdevice.set_volume(0.0) #set volume 0 for not hear the BEEEP
   mc = castdevice.media_controller
   url="http://" + local_ip + fname
   print(url)
   mc.play_media(url, "audio/wav")
   mc.block_until_active()
   mc.pause() #prepare audio and pause...
   time.sleep(1.0);

   if not volume is None:
      castdevice.set_volume(volume) 

   mc.play() #play the mp3
   castdevice.wait()
   # this is required
   time.sleep(1.0)
  
   # wait for it to be done
   while not mc.status.player_is_idle:
      castdevice.wait()
      time.sleep(0.5)

   if not volume is None:   
      castdevice.set_volume(vol_previous) 

   mc.stop()
   castdevice.quit_app()
   return  

#-------------------------------
# main for testing
#-------------------------------
def main(say, volume): 
   announce(say, volume) 

#--------------------------------
#  play a mp3 file 
#--------------------------------
def playmp3(soundfile, volume):

   if not soundfile.startswith(mp3dir):
       soundfile = mp3dir + soundfile

   systemvol = ""
   if not volume is None:
     if (float(volume) > 1):        # convert 0-100 to 0-1
       volume=float(volume)/100.0
     systemvol= " --gain " + str(round(float(volume), 2))
     systemvol= " --gain 0.9" 
        
   # play over pi speaker 
   if usePiSpeaker:
       cmd =  '/usr/bin/mpg321 -q ' + systemvol +  " /var/www/html" + soundfile  + ' &'
       print('cmd is ', cmd)
       os.system(cmd)

   if useGoogleHome:
     processes = []

     for address in broadcast_addresses:
        p = Process(target = speak, args=(address, soundfile, volume))
        processes.append(p)
        p.start()

     for process in processes:
        process.join()

     time.sleep(1.0)

#------------------------
# announce the text
#------------------------
def announce(text, volume=100):
   print("announce: " + text)
   soundfile = makefile(text)
   playmp3(soundfile, volume)


