
import paho.mqtt.client as mqtt
import time
import os
import psycopg2
from multiprocessing import Process

# topic with status
topic = 'home'
user = 'alarm'
host_name = 'alarm'
process = None

# count number of people who are home
statusquery = 'select count(person)  from (select distinct on (person,location) time, person, location, home from bluetooth order by person, location, time desc) a where home= true;'
insert_sql = "insert into bluetooth(time, location, person, home) values (to_timestamp(%s), %s, %s, %s );"
query_sql  = "select home from bluetooth where person = %s order by time desc limit 1"

currentCount = None  # number of people home

def on_connect(client, obj, flags, rc):
    client.subscribe(topic)
    print('subscribing',client, obj, flags,rc)


def on_message(client, userdata, message):
    msg =  str(message.payload.decode("utf-8")).split(",")
    print('recieved msg ', msg)
    time   = msg[0]
    locale = msg[1]
    person = msg[2]
    home   = msg[3]
    insert_record( (time, locale, person, home) )


def insert_record( values ):
    global currentCount
    time, locale, person, home = values

    homeb =  False
    if home == '1' or home == 1 or home == True:
        homeb = True

    print(home, homeb)
    print('insert_record values ', values)
    con = None
    try:
      con = psycopg2.connect('user=' + user )

      with con.cursor() as cur:
         cur.execute(query_sql, (person,) )
         status = cur.fetchone()[0]

         if status != homeb:
            print('db ', cur.mogrify(insert_sql, values ))
            cur.execute(insert_sql, values)
            con.commit()

      with con.cursor() as cur:
        cur.execute(statusquery)
        count = cur.fetchone()[0]
        if currentCount == None:
            currentCount = count

        currentCount = count
        print('current count', count)

    except:
       print("insert_record error", sys.exc_info()[0])
    finally:
        con.close


def main():
    client = mqtt.Client(client_id="bluetooth")
    print('loop connected to ', host_name)
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host_name)
    client.loop_forever()

# start process in thread
def start():
    global process
    process = Process(target=main,name='bluetooth')
    print('starting bluetooth listener')
    process.start()

def stop():
    print("stopping bluetooth process")
    process.terminate()

