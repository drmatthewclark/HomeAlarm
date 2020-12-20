
import paho.mqtt.client as mqtt
import time
import os
from multiprocessing import Process
import googlespeak

# topic with status
topic = 'home'
user = 'alarm'
host_name = 'alarm'
process = None

# count number of people who are home
statusquery = 'select count(person)  from (select distinct on (person,location) time, person, location, home from bluetooth order by person, location, time desc) a where home= true;'

currentCount = None  # number of people home

def on_message(client, userdata, message):
    msg =  str(message.payload.decode("utf-8")).split(",")
    time   = msg[0]
    locale = msg[1]
    person = msg[2]
    home   = msg[3]
    if home == 'away':
        home = False
    else:
        home = True

    insert_record(time, locale, person, home)



def insert_record(time, locale, person, home):
    global currentCount

    con = None
    try:
      con = psycopg2.connect('user=' + user )
      sql = "insert into bluetooth(time, location, person, home) values" \
           " (to_timestamp(%s), %s, %s, %s );"
      values = (time, locale, person, home)

      with con.cursor() as cur:
         #print(cur.mogrify(sql, values ))
         cur.execute(sql, values)
         con.commit()

      with con.cursor() as cur:
        cur.execute(statusquery)
        count = cur.fetchone()
        if currentCount == None:
            currentCount = count

        currentCount = count

    except:
       print("insert_record error", sys.exc_info()[0])
    finally:
        con.close


def main():
    client = mqtt.Client("sensor")
    client.on_message=on_message
    client.connect(host_name)
    client.loop_start()

    client.subscribe(topic)

    while(1):
       time.sleep(32067)
             
    client.loop_stop()

# start process in thread
def start():
    global process
    process = Process(target=main,name='bluetooth')
    process.start()

def stop():
    print("stopping bluetooth process")
    process.terminate()

