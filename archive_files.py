#! /usr/bin/env python
from datetime import datetime, timedelta
from MetProc import MetProc

print("BEGIN GEOS archiving ...")

day = timedelta(days=1)
now = datetime.now()

#days_back = 10
days_back = 70

# archive ...

for x in range(days_back,0,-1):
    date = now-x*day
    print(" ------------------")
    print(" archive : " + date.strftime("%x"))
    geosproc = MetProc(date,'/glade/scratch/fvitt/GEOS_test')

    validated = geosproc.check( 'validated' )
    archived = geosproc.check( 'archived' )

    if validated and not archived:
        ok = geosproc.archive( )

print("END GEOS archiving")

