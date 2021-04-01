#! /usr/bin/env python
from datetime import datetime, timedelta

date = datetime( 2000, 1, 30 )

date0 = datetime( 1900, 1, 1 )

times = [i * 3 for i in range(8)]  # hours

print(times)
#help(times)

dateslist = list()
days = list()

for hr in times :
    d = datetime( 2000, 1, 30, hr, 0, 0 )
    dd = d - date0
    #help(dd)
    ddd = dd.days + (dd.seconds/86400.0)
    print( dd.days,  dd.seconds, ddd)
    days.append( ddd )
    dateslist.append(d)

print(dateslist)
print(days)

print(' reference date : '+date0.strftime("%d/%m/%Y"))


