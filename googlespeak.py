#!/usr/bin/python3
import sys
import pychromecast
import os
import os.path
from gtts import gTTS
import time
import hashlib
from multiprocessing import Process
import datetime
# 
# addresses of google home devices
#
broadcast_addresses = {"192.168.20.11", "192.168.20.97" , "192.168.20.18", "192.168.20.20"}
#broadcast_addresses = {"192.168.20.97" } # basement
mp3dir="/5920ddcqeag/"    # system-dependent directory to cache sound files
useGoogleHome = True
usePiSpeaker  = True

#-----------------------------------------
# create the mp3 file for the text to say
#-----------------------------------------
def makefile(say):
   say = say.replace("_", " ")  # replace underscores

   tmppath= "/var/www/html" 
   fname= mp3dir + hashlib.md5(say.encode()).hexdigest()+".mp3"; #create md5 filename for caching

   if not os.path.isfile(tmppath+fname):
      tts = gTTS(say,lang='en')
      tts.save(tmppath+fname)

   return fname

#-------------------------------------
# say the words on google home
#-------------------------------------
def speak(ip, fname, volume):
   
   local_ip="192.168.20.26"

   castdevice = pychromecast.Chromecast(ip)
   castdevice.wait()
   vol_previous=castdevice.status.volume_level

   #castdevice.set_volume(0.0) #set volume 0 for not hear the BEEEP
   mc = castdevice.media_controller
   url="http://" + local_ip + fname
   mc.play_media(url, "audio/mp3")
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

   # play over pi speaker 
   if usePiSpeaker:
     os.system('/usr/bin/mpg321 ' + systemvol +  " /var/www/html" + soundfile  + ' &')

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
def announce(text, volume):
   print("announce: " + text)
   soundfile = makefile(text)
   playmp3(soundfile, volume)


