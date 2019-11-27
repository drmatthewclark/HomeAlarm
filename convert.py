#!/usr/bin/env python 
#
# alarm system using Honeywell sensors written in Python from the
# original awk implementation
# Matthew Clark 25 Nov 2019
#
import datetime
import os
import psycopg2
import sys
import json
import subprocess
import shlex

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
  status["bit1"]       = 1    #  ?
  status["bit2"]       = 2    #  ?
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
   sql = "select number, name, closed_bit, normal, loop1, loop2, loop3 from devices;"
   cur.execute(sql)
   for data in cur:
     result.append(data)
   
   return result;

#----------------------------------------------
# process a line of JSON code from the radio
#----------------------------------------------
def process(line):

  global lastalert
  guard_gap = 4.0
  flag = False
  parsed = json.loads(line)
  id = parsed["id"]
  time = parsed["time"]
  event = parsed["event"]

  timestamp = datetime.datetime.strptime(time,"%Y-%m-%d %H:%M:%S" )
  device = getdeviceinfo(id)

  if device is None:   # if device is not in list; a neighbors device
    return

  name = device["name"]
  hashkey = str(id) + 'x' + str(event)  # hash to store last signal

  # ignore the multiple signals from each device; process
  # only one within the guard_gap interval

  if (hashkey in lastalert):
    gap = (timestamp - lastalert[hashkey]).total_seconds()
    if (gap  < guard_gap):  # time gap between signals
       return

  lastalert[hashkey] = timestamp
  
  print(name + " " +  line)

  # is this a heartbeat or a signal?
  heartbeat = (4 & event) > 0  # true/false for heartbeat

  status_result = device["normal"]  # default status
  device_signal = event & device["code"]

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
    if (status[val] & device["code"] == 0 and (status[val] & event) > 0):
      status_result = val + "," + status_result

  print("status: " + status_result)

  # save the event into the database
  sql = "insert into events(source, event, code, flag) values( %s, %s, %s, %s)"
  values = (name, status_result, event, flag )
  cur.execute(sql, values)
  conn.commit()

  # if action is warranted:
  if flag:
    cmd = "nohup /home/pi/action.sh " + str(time) + " " + str(name) + " "  + str(status_result) + " " +  str(event) + " " + str(flag) + " >/dev/null &"

    print("take action " + cmd)
    subprocess.call(cmd, shell=True)


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
		   return result
	return None

#-------------------------
# main 
#-------------------------
def main():

  global deviceList, conn, cur, status, lastalert
  lastalert = dict()

  # connect to database
  conn = psycopg2.connect('user=alarm')
  cur = conn.cursor()
  deviceList  = readDevices()
  initstatus()
   
  # command to start radio
  #
  cmd="rtl_433 -p 0 -f 345000000 -s 1M -R 70 -F json"

  file = subprocess.Popen(shlex.split(cmd), bufsize=1,stdout=subprocess.PIPE, stdin=subprocess.PIPE) 
  while True:
   line = file.stdout.readline().rstrip() 
   process(line)

main()
