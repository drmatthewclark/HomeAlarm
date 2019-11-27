#!/bin/bash -x
#
# say something
#  pico2wave settings:
#   <pitch level='400'>   change pitch
#   <volume level='50'>  change volume
#
# languages:
#
# English en-US
# English en-GB
# French fr-FR
# Spanish es-ES
# German de-DE
# Italian it-IT

TEXT="$1"
PITCH=150
VOLUME=50
LANG=en-US
FIXED=`echo "${TEXT}" | sed -r 's/(_)|([|])/ /g'`

TEMP="/var/www/html/5920ddcqeag/`echo ${FIXED}  ${PITCH} ${VOLUME} | /usr/bin/md5sum | sed -r 's/(\s+)|(-)//g'`.wav"

if [ ! -e "${TEMP}" ]; then
  pico2wave -l ${LANG}  -w ${TEMP}  "<pitch level='${PITCH}'> <volume level='${VOLUME}'>${FIXED}  ."  
fi

if [ -e "${TEMP}" ]; then
    aplay --device="plughw:0,0" "${TEMP}"  > /dev/null 2>&1  
fi


/home/pi/google-speak "${TEXT}"  ${VOLUME}
