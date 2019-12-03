#!/usr/bin/env python3

import googlespeak as gs 
import psycopg2 as psql
import os

conn = psql.connect(user='alarm')
cur = conn.cursor()

#--------------------------------------------
# get settings for which alarms are enabled
#--------------------------------------------
def get_status():
   cur.execute("select category, enabled from state;")
   status = dict()
   for state in cur.fetchall():
      status[state[0]] = state[1]

   return status


#--------------------------------
# send mail/text notifications
#--------------------------------
def smail(text):
  cur.execute("select contact from contacts;")
  for contact in cur.fetchall():
    email = contact[0]
    cmd="echo " + text + '| mail -s "ALARM: "' + text + " " + email
    log_action("email " + email, "alarm")
    os.system("echo " + text + '| /usr/bin/mail -s "ALARM: "' + text + " " + email)


#----------------------------
# log an action into the db
#----------------------------
def log_action(action, cause):
  sql="insert into actions (action, cause) values (%s, %s);"
  tuple=(action, cause)
  cur.execute(sql, tuple)
  conn.commit()
  return None


#-----------------------------------------------
# set the trigger flag when alarm is triggered
#-----------------------------------------------
def trigger():
   cmd="update state set enabled = true where category = 'triggered';"
   cur.execute(cmd)
   conn.commit()


