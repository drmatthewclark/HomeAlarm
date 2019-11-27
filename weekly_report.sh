#!/bin/bash
#
#
source /home/pi/functions.sh

table="`/home/pi/summary`"

smail  "weekly summary"    "${table}"

