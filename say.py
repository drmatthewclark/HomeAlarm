#!/usr/bin/python3

import googlespeak
import sys 

text = ""
for i in range(1, len(sys.argv)):
        text += " " + sys.argv[i]

googlespeak.main(text , 15)

