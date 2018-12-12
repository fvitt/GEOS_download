#! /usr/bin/env python
from datetime import datetime, timedelta

day = timedelta(days=1)
hour = timedelta(hours=1)
minute = timedelta(minutes=1)

now = datetime.now()
#later = now+(5*minute)
#
#print later.strftime("%H:%M")

date = now-22*day
print date

for x in range(0,20):
    date = now-x*day
    print " dir : "+date.strftime("Y%Y/M%m/D%d")
    yr = date.strftime("%Y")
    mon = date.strftime("%m")
    dom = date.strftime("%d")
    print " -------> proc_goes -year "+yr+" -month "+mon+" -day "+dom

print xyz


