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
#
#
# warn if the temperature is close to freezing or overheating
#
import psycopg2 as psql
import time
import random
from multiprocessing import Process
import googlespeak as gs
import functions

volume = 80
process = None

def checkTemperature():
  LO_TEMP="38"
  HI_TEMP="115"

  query="select distinct on(name) name, round(temperature::numeric, 0) \
            from data where time = (select max(time) from temperature) \
            and (name != 'outside' and name not like 'hvac%%') \
            and (temperature < %s or temperature > %s) \
            group by name, time, temperature;"

  vals=(LO_TEMP, HI_TEMP)

  conn = psql.connect(user='sensor', host='pi')
  with conn.cursor() as cur:
    cur.execute(query, vals)
    for dev in cur.fetchall():
       name = str(dev[0]).replace("1","")
       temp = str(dev[1])
       warn = "temperature warning " + name + " " + temp + " degrees "
       print(warn)
       functions.smail(warn)
       gs.announce(warn, volume)

  conn.close()

def warn():
    print("starting temperature monitor")
    while True:
        checkTemperature()
        time.sleep(60 + random.randint(-10, 10))

def start():
    global process
    process = Process(target = warn, name = 'temperature')
    process.start()

def stop():
    print("stopping temperature process")
    process.terminate()
