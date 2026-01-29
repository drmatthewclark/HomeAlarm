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
along with HomeAlarm.  If not, see <https://www.gnu.org/licenses/>.

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
from logsetup import logsetup
from datetime import datetime

logger = logsetup('temperature')
last_time = datetime( day=1,month=1,year=2000 )

volume = 80
process = None
running = True
host = 'pi'
SLEEP_TIME = 60 * 60 * 4  # seconds between notifications
LO_TEMP = "35"
HI_TEMP = "115"

def getSilent():
    status = functions.get_status()
    return status["silent-alarm"]


def checkTemperature():
    global last_time

    query = "select distinct on(name) name, round(temperature::numeric, 0) \
            from data where time = (select max(time) from temperature) \
            and (name != 'outside' and name not like 'hvac%%' ) \
            and (temperature < %s or temperature > %s) \
            group by name, time, temperature;"

    vals = (LO_TEMP, HI_TEMP)
    conn = None
    try:
        conn = psql.connect(user='sensor', host=host)
    except:
        logger.error(f'check_temperature: error connecting to host {host}')
        return

    time = datetime.now()
    interval = time - last_time
    #print(f"temperature monitor query {interval}")

    with conn.cursor() as cur:
        cur.execute(query, vals)
        for dev in cur.fetchall():
            name = str(dev[0]).replace("1", "")
            temp = str(dev[1])
            warn = f"temperature warning {name} {temp} degrees"
            logger.info( warn )
            #print(warn) 

            if interval.total_seconds() > SLEEP_TIME:
               #print(warn)

               logger.warning(warn)
               functions.smail(warn)
               if not getSilent():
                   gs.announce(warn, volume)
               last_time = time
        
    conn.close()


def warn():
    while running:
        checkTemperature()
        time.sleep(120)


def start():

    logger.info("starting temperature monitor")
    global process
    process = Process(target=warn, name='temperature')
    process.start()


def stop():
    global process
    global running
    logger.info("stopping temperature process")
    running = False

if __name__ == '__main__':
   start()
