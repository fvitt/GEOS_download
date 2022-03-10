#! /usr/bin/env python
import netCDF4 as nc
import math
import glob

def check(filepath, tods):

    #print("Check time and datesec in : "+filepath)
    ds = nc.Dataset(filepath)
    datesecs = ds['datesec'][:]
    times = ds['time'][:]
    i=0
    for t in times:
        x, y = math.modf(t)
        if datesecs[i] != tods[i]:
            print("Incorrect datesec in :"+filepath)
            print(datesecs)
            return False
        if x != float(tods[i])/86400.:
            print("Incorrect time in :"+filepath)
            print(times)
            return False
        i=i+1

    ds.close()

    return True

def check_all_files():
    print('Begin Test ...')


    tods = [ 0, 10800, 21600, 32400, 43200, 54000, 64800, 75600 ]

    print(" ")
    print(" ")

    #for yr in range(2015,2022):
    for yr in range(2021,2022):
        print('Check year ',yr)

        dir = '/glade/p/cesm/chwg_dev/met_data/GEOS5/orig_res/'+str(yr)
        print('check files in: '+dir)
        files = glob.glob(dir+'/*.nc')
        for f in files:
            ok = check(f, tods)

        dir = '/glade/p/cesm/chwg_dev/met_data/GEOS5/0.9x1.25/'+str(yr)
        print('check files in: '+dir)
        files = glob.glob(dir+'/*.nc')
        for f in files:
            ok = check(f, tods)

        dir = '/glade/p/cesm/chwg_dev/met_data/GEOS5/'+str(yr)
        print('check files in: '+dir)
        files = glob.glob(dir+'/*.nc')
        for f in files:
            ok = check(f, tods)

    print(" ")
    print(" ")


    print('END Test')
