#
#
# warn if the temperature is close to freezing or overheating
#
import psycopg2 as psql
import time
import random
from multiprocessing import Process
import googlespeak as gs

conn = psql.connect(user='sensor', host='pi')

def checkTemperature():
  LO_TEMP="38"
  HI_TEMP="115"

  query="select distinct on(name) name, round(temperature::numeric, 0) \
            from data where time = (select max(time) from temperature)\
            and (name != 'outside' and name not like 'hvac%%') \
            and (temperature < %s or temperature > %s)\
            group by name, time, temperature;"

  vals=(LO_TEMP, HI_TEMP,)

  with conn.cursor() as cur:
    cur.execute(query, vals)

    for dev in cur.fetchall():
       name = str(dev[0])
       temp = str(dev[1])
       warn = "temperature warning " + name + " " + temp
       print(warn)
       gs.announce(warn)


def warn():
    print("starting temperature monitor")
    while True:
        checkTemperature()
        time.sleep(60 + random.randint(-10, 10))

def check():
    Process(target = warn).start()



check()
