#!/bin/bash
#
# script to create a continuous fire alarm until turned off.  
# We presume that the actual fire alarm devices will also be making noise
# called with name of fire device as argument

source /home/pi/functions.sh
test=false

while [ `${PSQL} "select enabled from state where category = 'triggered';"` = t ] || [ ${test} = true ]; do
  speak "FIRE_FIRE_FIRE_${1}"  1.0
  beep  1
done

