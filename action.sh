#!/bin/bash
#
# called by trigger on event with this kind of argument:
#
# 2019-08-01 20:31:43.018812 motion_waverly motion t 128 892860
# 2019-10-18 22:37:44 motion_waverly motion 128 true
#    date         time            source     event flag code source-code
#
IFS=$'\n'
source /home/pi/functions.sh

#----------------------
# something is on fire
#---------------------
function fire() {
  

  # if already triggered, skip
  isEnabled triggered && return 0
  trigger   
  log_action "fire alarm" ${name} fire
  smail fire ${name}

# persistent alarm
 /bin/bash -c "nohup ${BASE}/fire_alert.sh ${name} &" 

}

#--------------------
# water
#-------------------
function water() {

  # if already triggered, skip
  isEnabled triggered && return 0
  trigger
  log_action "water alert" $name water 
  smail water ${name}

# persisten alarm

 /bin/bash -c "nohup ${BASE}/water_alert.sh ${name} &" 

}




#---------------------------------
# sound the alarm from all sensors
#--------------------------------
function alarm_away() {

  # if already triggered, skip
  isEnabled triggered && return 0
  trigger
  log_action "alarm " $name alarm
  smail alarm ${name}

  ! isEnabled silent-alarm  && /bin/bash -c "nohup ${BASE}/alarm_alert.sh ${name} &" 
}



#-------------------------------------------
# sound alarm only from peripheral sensors, 
# not from internal motion sensors
#-------------------------------------------
function alarm_stay() {

if [[ $source != *"motion"* ]]; then
  alarm_away $@
fi

}



#------------------------------------------
# chime if a door is opened
#------------------------------------------
function door_alert() {

  if [[ $source != *"motion"* ]] && [[ $source != *"water"*  ]]; then
    log_action "door alert" ${name} door
    ${BASE}/beep.sh door_alert ${name}
  fi
}

#------------------------------------------
# speak about low battery
#------------------------------------------
function battery_alert() {

  log_action "battery alert" $name battery
  ${BASE}/beep.sh battery_low  \"${name}\"
}


#---------------------------------------------
# part that gets executed follows

#
# find what alarms are currently enabled
#
states="${PSQL} \"select category,enabled from state;\""
states=`eval ${states}`
name=$3
source=$3
event=$4

#
# events always processed; important enough not to need
# an enabled state
#
#  fire

if [[ $source == *"fire"* ]]; then
   fire $@
   exit
fi


if [[ $source == *"water"* ]]; then
   water $@
   exit
fi



#
# loop through enabled states to take action
# ordered by priority
#
for row in ${states}; do 

case ${row} in
        'alarm-away|t')
	 alarm_away $@
	 break
	;;
        'alarm-stay|t')
         alarm_stay $@
	 break
	;;
	'door alert|t')
 	 door_alert $@
         echo "door_alert " $@  >> /tmp/alert.log
	 break
	;;
  esac

# after all others
# battery low signal
#
  if [[ ${event} == *"battery"* ]]; then
     battery_alert $@
  fi

done
