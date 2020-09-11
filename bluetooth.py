#!/usr/bin/python3

import paho.mqtt.client as mqtt
import time
import os
import psycopg2
import sys

# topic with status
topic = 'home'
user = 'alarm'
host_name = 'alarm'

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


main()
