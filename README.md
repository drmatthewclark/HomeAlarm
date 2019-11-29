#Repurpose Honeywell wireless sensors from an ADT system into a better interface          
Features
- web/touch interface for remote operation
- door alert
- home alarm/away alarm
- email/text notification when alarm goes off
- uses Google home to sound messages/alarms
- lists last event for each device
- lists devices that have not sent signal in a day
- optional list temperature sensors
- stores all events in a database for analysis

![Screenshot](./screenshot.png)

required packages
	postgresql
	rtl_433
	psycopg2
        pychromecast
	gtts
	pico2wave
