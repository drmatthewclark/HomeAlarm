#!/usr/bin/env python3
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

import psycopg2 as psql
import os


#--------------------------------------------
# get settings for which alarms are enabled
#--------------------------------------------
def get_status():
   conn = psql.connect(user='alarm')
   with conn.cursor() as cur:
     cur.execute("select category, enabled from state;")
     status = dict()
     for state in cur.fetchall():
        status[state[0]] = state[1]

   conn.close()
   return status


#--------------------------------
# send mail/text notifications
#--------------------------------
def smail(text):
   conn = psql.connect(user='alarm')
   with conn.cursor() as cur:
      cur.execute("select contact from contacts where type = 'email';")
      for contact in cur.fetchall():
        email = contact[0]
        cmd="echo " + text + '| mail -s "ALARM: "' + text + " " + email
        log_action("email " + email, "alarm")
        os.system("echo " + text + '| /usr/bin/mail -s "ALARM: "' + text + " " + email)
   conn.close()

#----------------------------
# log an action into the db
#----------------------------
def log_action(action, cause):

    sql="insert into actions (action, cause) values (%s, %s);"
    tuple=(action, cause)
 
    conn = psql.connect(user='alarm')
    with conn.cursor() as cur:
      cur.execute(sql, tuple)
    conn.commit()
    conn.close()

    return None


#-----------------------------------------------
# set the trigger flag when alarm is triggered
#-----------------------------------------------
def trigger():
   cmd="update state set enabled = true where category = 'triggered';"
   conn = psql.connect(user='alarm')
   with conn.cursor() as cur:
     cur.execute(cmd)
   conn.commit()
   conn.close()
