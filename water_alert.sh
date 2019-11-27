#!/bin/bash
#
# script to gove a specific water related alarm with a custom water beep
# alarm every 2 minutes.  Called with the name of the device reporting water
# as the first argument
#
source /home/pi/functions.sh
DELAY="120s"

test=false 

#
# loop until the alarm is turned off
#
while [ `${PSQL} "select enabled from state where category = 'triggered';"` = t ] || [ "${test}" = true ] ; do
  beep  2
  speak "water_detected ${1}"
  sleep ${DELAY}
done

