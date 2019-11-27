
PSQL="/usr/bin/psql -At -U alarm -c "
BASE="/home/pi"

#-------------------
# speak some words 
#-------------------
function speak() {
 ${BASE}/speak.sh $@
 echo ${BASE}/speak.sh $@
}



#-------------------
# play a sound file
#--------------------
function play() {
 /usr/bin/aplay $@  
 #echo /usr/bin/aplay $@ 
 echo ${BASE}/google-play  $@ 
}

#---------------------
# send a mail message
#--------------------=
function smail() {

  contacts="${PSQL} \"select contact from contacts;\""
  contacts=`eval $contacts`

  for dest in ${contacts}; do
    echo  "$@"  | mail -s "ALARM: $1" $dest
    log_action email $dest $1
  done
}

#-----------------------
# log activity
# log_action <string description> <string cause>
#----------------------
function log_action() {
  temp="${PSQL} \"insert into actions (action, cause) values ('$1: $2','$3');\""
  temp=`eval ${temp}`
}

#---------------------
# set triggered flag
#--------------------
function trigger() {
  temp="${PSQL} \"update state set enabled = true where category = 'triggered'\";"
  temp=`eval ${temp}`
}

#---------------
# return triggered status
#  e.g. isEnabled triggered
#---------------
function isEnabled () {

  val="${PSQL} \"select enabled from state where category = '${1}';\""
  val=`eval ${val}`

  if  [ "${val}" = t ]; then
	return 0
  fi 

  return 1 

}

#--------------------
# make some noise
# beep <beep code>
#------------------
function beep() {
   ${BASE}/beep.sh $1
}
