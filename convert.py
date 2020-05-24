#!/usr/bin/python3 
#
# alarm system using Honeywell sensors written in Python from the
# original awk implementation
# Matthew Clark 25 Nov 2019
#


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
import datetime
import os
import psycopg2
import sys
import json
import subprocess
import shlex
import action
from multiprocessing import Process
import temperature_warning as temp_warn

#
# initialize the status bits for Honeywell sensors
#
def initstatus():
#
# status bits some devices have more than one signal bit, or 'loop'
# that might be set. e.g. door devices have a wired terminal and
# water/smoke alarms can signal lo/hi temperature warnings
#
#
# bit   value   use
# 0     1       unknown
# 1     2       unknown
# 2     4       heartbeat signal
# 3     8       low battery
# 4     16      loop3 signal
# 5     32      loop2 signal
# 6     64      tamper switch
# 7     128     loop1 sisgnal

  global status
  status = dict()
  status["bit1"]       = 1    #  ? not sure what this means  
  status["bit2"]       = 2    #  ? not sure what this means
  #status["heartbeat"] = 4    # periodic signal; suppresed
  status["battery"]    = 8    # battery is low
  #status["loop3"]     = 16   # loop 3
  #status["loop2"]     = 32   # loop 2
  status["tamper"]     = 64   # tamper switch activated
  #status["loop1"]     = 128  # loop 1
  return status

#---------------------------------------------
# read the list of devices from the database
#  return a list of devices with info
#---------------------------------------------
def readDevices():

  result = list()
  sql = "select number, name, closed_bit, normal, loop1, loop2, loop3, type  from devices;"

  conn = psycopg2.connect(user='alarm')
  with conn.cursor() as cur:
       cur.execute(sql)
       for data in cur:
         result.append(data)
  
  conn.close()
  return result

#----------------------------------------------
# process a line of JSON code from the radio
#----------------------------------------------
def process(line):

  global lastalert
  guard_gap = 3.5  # seconds
  flag = False

  try:
    parsed = json.loads(line)
  except:
    print("eror json parsing: " + line)
    return

  deviceId = parsed["id"]
  eventTime = parsed["time"]
  eventCode = parsed["event"]

  timestamp = datetime.datetime.strptime(eventTime,"%Y-%m-%d %H:%M:%S" )
  device = getdeviceinfo(deviceId)

  if device is None:   # if device is not in list; a neighbors device
    return

  deviceName = device["name"]
  deviceType = device["type"]

  hashkey = str(deviceId) + 'x' + str(eventCode)  # hash to store last signal

  # ignore the multiple signals from each device; process
  # only one within the guard_gap interval

  if (hashkey in lastalert):
    gap = (timestamp - lastalert[hashkey]).total_seconds()
    if (gap  < guard_gap):  # time gap between signals
       return

  lastalert[hashkey] = timestamp
  

  # is this a heartbeat or a signal?
  heartbeat = (4 & eventCode) > 0  # true/false for heartbeat

  status_result = device["normal"]  # default status
  device_signal = eventCode & device["code"]

  if (device_signal > 0 ):
        if not heartbeat:
            flag = True  # means that an action will be taken

        status_result = "" 
        if (device_signal & 128):
            status_result += device["loop1"]
        if (device_signal & 32):
            status_result += device["loop2"]
        if (device_signal & 16):
            status_result += device["loop3"]

  # check other stati - battery, tamper etc.
  for val in status:
    if (status[val] & device["code"] == 0 and (status[val] & eventCode) != 0):
      status_result = status_result + "," + val

  print("status: " + status_result)

  # save the event into the database
  sql = "insert into events(source, event, code, flag) values( %s, %s, %s, %s)"
  values = (deviceName, status_result, eventCode, flag)

  conn = psycopg2.connect(user='alarm')
  with conn.cursor() as cur:
    cur.execute(sql, values)

  conn.commit()
  conn.close()

  print(deviceName + " flag:" + str(flag) + " " +  line)
  # if action is warranted:
  #
  if flag:
    startThread(action.action, (deviceName, status_result, deviceType))


#-------------------------------------------
# given the id from the radio return the
# device information
#-------------------------------------------
def getdeviceinfo(id):
	for data in deviceList:
		if (id == data[0] ):
                   result = dict()
                   result["id"]     = data[0]
                   result["name"]   = data[1]
                   result["code"]   = data[2]
                   result["normal"] = data[3]
                   result["loop1"]  = data[4]
                   result["loop2"]  = data[5]
                   result["loop3"]  = data[6]
                   result["type"]   = data[7]
                   return result
	return None


#
# start a function in a thread
#
def startThread(funcname, args):
      if args is None:
          arg = ""
      else:
          arg = str(args) 

      print("start action thread " + funcname.__name__ + " " + arg)
      Process(target = funcname, args=args).start()


#-------------------------
# main 
#-------------------------
def main():
  # start temperature monitor
  temp_warn.check()

  global deviceList, status, lastalert
  lastalert = dict()

  # connect to database
  deviceList  = readDevices()
  initstatus()
   
  # command to start radio
  #
  cmd="rtl_433 -p 0 -f 345000000 -s 1M -R 70 -F json"

  file = subprocess.Popen(shlex.split(cmd), bufsize=1,stdout=subprocess.PIPE, stdin=subprocess.PIPE) 
  while True:
   line = file.stdout.readline().decode("UTF-8").rstrip()
   process(line)

main()
