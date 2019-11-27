#!/bin/bash
#
# custom burglar alarm that continues until shut off
#
source /home/pi/functions.sh

#beep 1
speak "$1 alarm triggered alarm triggered"
#beep 1
#beep 1
#sleep 5
sleep 4
test=false

while isEnabled 'triggered' || [ ${test} = true ]; do
  speak "alarm_alarm_alarm_$1_police_dispatch_confirmed"  1.0
  play  /home/pi/recordings/sirenhilowithrumbler.wav  
done

