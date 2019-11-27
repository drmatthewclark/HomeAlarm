#!/bin/bash
#
# make different beeps based on argument
# arguments (door_alert,1,2,3,4)

source /home/pi/functions.sh

function beep1() {
( speaker-test -t sine -c 2 -s 2 -f 800 & TASK_PID=$! ; sleep 0.09 ; kill -s SIGINT $TASK_PID ) > /dev/null
( speaker-test -t sine -c 2 -s 2 -f 1000 & TASK_PID=$! ; sleep 0.09 ; kill -s SIGINT $TASK_PID ) > /dev/null
( speaker-test -t sine -c 2 -s 2 -f 800 & TASK_PID=$! ; sleep 0.09 ; kill -s SIGINT $TASK_PID ) > /dev/null
( speaker-test -t sine -c 2 -s 2 -f 1000 & TASK_PID=$! ; sleep 0.09 ; kill -s SIGINT $TASK_PID ) > /dev/null
}

function beep2() {
( speaker-test -t sine -c 2 -s 2 -f 1500 & TASK_PID=$! ; sleep 0.09 ; kill -s SIGINT $TASK_PID ) > /dev/null
( speaker-test -t sine -c 2 -s 2 -f 900 & TASK_PID=$! ; sleep 0.09 ; kill -s SIGINT $TASK_PID ) > /dev/null
}


function beep3() {
( speaker-test -t sine -c 2 -s 2 -f 900 & TASK_PID=$! ; sleep 0.2 ; kill -s SIGINT $TASK_PID ) > /dev/null
}


function beep4() {
( speaker-test -t sine -c 2 -s 2 -f 2000 & TASK_PID=$! ; sleep 0.2 ; kill -s SIGINT $TASK_PID ) > /dev/null
}

function door_alert() {

    amixer set PCM -- 85%
    beep4
    speak "$1" 
    amixer set PCM -- 100%
}



case $1 in 
  door_alert)
    door_alert "$2"
    ;;
  battery_low)
    door_alert "$2 battery low "
    ;;
  1)
    beep1
    beep4
    sleep 1
    beep1
    sleep 1
    beep1
    beep4
  ;;
  2)
    beep2
    sleep 1
    beep2
  ;;
  3)
    beep3
    sleep 2
    beep3
    sleep 2
    beep3
  ;;
  4)
  beep4
  sleep .1 
  beep4
  ;; 
esac


