#! /usr/bin/env python
from datetime import datetime, timedelta
from MetProc import MetProc

print("BEGIN GEOS processing ...")

day = timedelta(days=1)
now = datetime.now()

#days_back = 10
days_back = 20

# check if data is download for past <days_back>+1 days ...

for x in range(days_back+1,0,-1):
    date = now-x*day
    print(" ------------------")
    print(" check download : " + date.strftime("%x"))
    geosproc = MetProc(date,'/glade/scratch/fvitt/GEOS')

    downloaded = geosproc.check( 'downloaded' )
    if not downloaded :
        ok = geosproc.download( )

# check if data has been combined for past <days_back> days
for x in range(days_back,0,-1):
    date = now-x*day
    print(" ------------------")
    print(" check combined : " + date.strftime("%x"))
    geosproc = MetProc(date,'/glade/scratch/fvitt/GEOS')

    downloaded = geosproc.check( 'downloaded' )
    combined = geosproc.check( 'combined' )
    if downloaded and not combined :
        ok = geosproc.combine( )

# check if data has been regridded for past <days_back> days
for x in range(days_back,0,-1):
    date = now-x*day
    print(" ------------------")
    print(" regrid : " + date.strftime("%x"))
    geosproc = MetProc(date,'/glade/scratch/fvitt/GEOS')

    combined = geosproc.check( 'combined' )

    regridded = geosproc.check( 'regridded' )
    if combined and not regridded :
        ok = geosproc.regrid( )

    regridded_1deg = geosproc.check( 'regridded_1deg' )
    if combined and not regridded_1deg :
        ok = geosproc.regrid_1deg( )

# validate ...

for x in range(days_back,0,-1):
    date = now-x*day
    print(" ------------------")
    print(" validate : " + date.strftime("%x"))
    geosproc = MetProc(date,'/glade/scratch/fvitt/GEOS')

    regridded = geosproc.check( 'regridded' )
    validated = geosproc.check( 'validated' )

    if regridded and not validated :
        ok = geosproc.validate( )

    regridded_1deg = geosproc.check( 'regridded_1deg' )
    validated_1deg = geosproc.check( 'validated_1deg' )

    if regridded_1deg and not validated_1deg :
        ok = geosproc.validate_1deg( )

# archive ...

for x in range(days_back,0,-1):
    date = now-x*day
    print(" ------------------")
    print(" archive : " + date.strftime("%x"))
    geosproc = MetProc(date,'/glade/scratch/fvitt/GEOS')

    validated = geosproc.check( 'validated' )
    archived = geosproc.check( 'archived' )

    if validated and not archived:
        ok = geosproc.archive( )

## clean up ....
#
#for x in range(days_back+10,days_back+30):
#    date = now-x*day
#    print(" ------------------")
#    print(" clean up : " + date.strftime("%x"))
#    geosproc = MetProc(date,'/glade/scratch/fvitt/GEOS')
#
#    archived = geosproc.check( 'archived' )
#    if archived :
#        ok = geosproc.cleanup( )

print("GEOS processing DONE")
