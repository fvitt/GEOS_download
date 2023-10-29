#! /usr/bin/env python
import xarray as xr
import os
import numpy as np
import glob
from datetime import datetime, timedelta
import pandas as pd

def combine_met_data( rootdir, date, ofilepath ) :

    #
    # Set the dirs based on date
    #
    day = timedelta(days=1)
    date0 = date-day

    dir0 = rootdir + "/" + date0.strftime("Y%Y/M%m/D%d")
    dir1 = rootdir + "/" + date.strftime("Y%Y/M%m/D%d")

    #print("dir0: ",dir0)
    #print("dir1: ",dir1)

    coord_ds = xr.open_dataset('/glade/work/fvitt/GEOS/GEOS5_orig_res_20180715.nc')
    lndfr_ds = xr.open_dataset('/glade/work/fvitt/GEOS/GEOS.fp.asm.const_2d_asm_Nx.00000000_0000.V01.nc4')
    lfr = lndfr_ds.FRLAND.values[0]

    rad_filem = glob.glob(dir0+'/GEOS.fp.asm.tavg1_2d_rad_Nx.*_2330.V01.nc4' )
    rad_files = glob.glob(dir1+'/GEOS.fp.asm.tavg1_2d_rad_Nx.*.V01.nc4')
    rad_files.sort()
    rad_filepaths = rad_filem + rad_files
    #print("rad_filepaths:")
    #print(rad_filepaths)

    flx_filem = glob.glob(dir0+'/GEOS.fp.asm.tavg1_2d_flx_Nx.*_2330.V01.nc4' )
    flx_files = glob.glob(dir1+'/GEOS.fp.asm.tavg1_2d_flx_Nx.*.nc4')
    flx_files.sort()
    flx_filepaths = flx_filem + flx_files

    lnd_filem = glob.glob(dir0+'/GEOS.fp.asm.tavg1_2d_lnd_Nx.*_2330.V01.nc4' )
    lnd_files = glob.glob(dir1+'/GEOS.fp.asm.tavg1_2d_lnd_Nx.*.nc4')
    lnd_files.sort()
    lnd_filepaths = lnd_filem + lnd_files

    asm_files = glob.glob(dir1+'/GEOS.fp.asm.inst3_3d_asm_Nv.*.nc4')
    asm_files.sort()

    xds = []
    dates = []
    datesecs = []

    print(" time average every 3 hours ...")
    # time average every 3 hours
    for n in range(0,8):
       hr = n*3
       #print("  hr: ",hr)
       rad_file1 = xr.open_dataset(rad_filepaths[hr])
       rad_file2 = xr.open_dataset(rad_filepaths[hr+1])
       flx_file1 = xr.open_dataset(flx_filepaths[hr])
       flx_file2 = xr.open_dataset(flx_filepaths[hr+1])
       lnd_file1 = xr.open_dataset(lnd_filepaths[hr])
       lnd_file2 = xr.open_dataset(lnd_filepaths[hr+1])

       ds1 = xr.Dataset( data_vars = {'ALB':rad_file1.ALBEDO, 'TS':rad_file1.TS, 'FSDS':rad_file1.SWGDN, 
                                      'SHFLX':flx_file1.HFLUX, 'TAUX':flx_file1.TAUX,'TAUY':flx_file1.TAUY, 'QFLX':flx_file1.EVAP,
                                      'SNOWH':lnd_file1.SNOMAS, 'SOILW':lnd_file1.GWETTOP, 'ORO':flx_file1.FRSEAICE })
       ds2 = xr.Dataset( data_vars = {'ALB':rad_file2.ALBEDO, 'TS':rad_file2.TS, 'FSDS':rad_file2.SWGDN, 
                                      'SHFLX':flx_file2.HFLUX, 'TAUX':flx_file2.TAUX,'TAUY':flx_file2.TAUY, 'QFLX':flx_file2.EVAP,
                                      'SNOWH':lnd_file2.SNOMAS, 'SOILW':lnd_file2.GWETTOP, 'ORO':flx_file2.FRSEAICE } )

       ds = xr.concat( [ds1,ds2], dim='time' )
       newtime = ds.time.mean() #0.5*( ds.time[0] + ds.time[1] )
       dt = pd.to_datetime(str(newtime.values))
       date = int(dt.strftime("%Y%m%d"))
       hour = int(dt.strftime("%H"))
       min = int(dt.strftime("%M"))
       sec = int(dt.strftime("%S"))
       datesec = (hour*60*60) + (min*60) + sec

       ds3 = (ds.interp(time=newtime)).astype(np.float32)

       ds3.ORO.values = np.where(ds3.ORO.values>0.5,2.0,lfr)

       file_3d = xr.open_dataset(asm_files[n])

       ds4 = xr.merge( [ds3, xr.Dataset( { 'T':file_3d.T, 'U':file_3d.U, 'V':file_3d.V, 'Q':file_3d.QV, 'PS':file_3d.PS, 'PHIS':file_3d.PHIS } )] )
       xds.append( ds4 )
       
       dates.append(date)
       datesecs.append(datesec)

       file_3d.close()
       rad_file1.close()
       rad_file2.close()
       flx_file1.close()
       flx_file2.close()
       lnd_file1.close()
       lnd_file2.close()

    #print("********************************************")
    print(" concat datasets ...")
    out_ds = xr.concat( xds, dim='time' )
    nlons = out_ds.lon.size
    nroll = int(nlons/2)
    #print("********************************************")
    print(" prepare output dataset ...")
    out_ds = out_ds.roll(lon=nroll,roll_coords=True)
    out_ds = out_ds.assign_coords(lon=out_ds.lon % 360 ) #.sortby('lon')
    out_ds.lon.attrs={'units':"degrees_east", 'long_name':"longitude" }
    out_ds = out_ds.assign_coords(lev=coord_ds.lev )

    out_ds.TAUX.values = -1.*out_ds.TAUX.values
    out_ds.TAUY.values = -1.*out_ds.TAUY.values

    out_ds.TAUX.attrs = flx_file1.TAUX.attrs
    out_ds.TAUY.attrs = flx_file1.TAUY.attrs

    out_ds.SHFLX.attrs = flx_file1.HFLUX.attrs
    out_ds.QFLX.attrs = flx_file1.EVAP.attrs
    out_ds.SNOWH.attrs = lnd_file1.SNOMAS.attrs
    out_ds.SOILW.attrs = lnd_file1.GWETTOP.attrs

    out_ds.ALB.attrs = rad_file1.ALBEDO.attrs
    out_ds.TS.attrs = rad_file1.TS.attrs
    out_ds.FSDS.attrs = rad_file1.SWGDN.attrs
    out_ds.ORO.attrs = lndfr_ds.FRLAND.attrs

    out_ds['SNOWH'] = out_ds.SNOWH.fillna(value=0.0)

    #print("********************************************")

    out_ds = xr.merge( [out_ds, xr.Dataset( { "hyam":coord_ds.hyam,"hybm":coord_ds.hybm,"hyai":coord_ds.hyai,"hybi":coord_ds.hybi } )] )

    #print("********************************************")
    #print(" construct date_ds dataset...")
    date_ds = xr.Dataset( data_vars={ "date":(["time"],dates), 
                                      "datesec":(["time"],datesecs) },
                                      coords={"time":(["time"],out_ds.time.values)} )
    date_ds.date.attrs['units'] = "current date (YYYYMMDD)"
    date_ds.date.attrs['long_name'] = "current date (YYYYMMDD)" 
    date_ds.datesec.attrs['units'] = "seconds"
    date_ds.datesec.attrs['long_name'] = "current seconds of current date" 

    #print(date_ds)
    #print("********************************************")
    #print("merge in date_ds  ...") 
    out_ds = xr.merge( [out_ds, date_ds] )

    #print("********************************************")
    out_ds.time.attrs.clear()
    out_ds.time.encoding = {'units':'days since 1900-01-01 00:00:00', 'calendar':'gregorian' }
    out_ds.time.attrs['long_name']='days since 1900-01-01 00:00:00'

    now = datetime.now()

    out_ds.attrs['history'] = 'created '+now.ctime()+ ' by '+os.environ.get('USER')
    out_ds.attrs['script']  = os.path.abspath(__file__)

    print(" dump data to: "+ofilepath+" ... ")

    out_ds.to_netcdf( ofilepath, unlimited_dims = ['time'] )
    out_ds.close()

    return True

def _test() :

    print('Begin TEST')

    time0 = datetime.now()

    rootdir = '/glade/scratch/fvitt/GEOS_test'
    date = datetime(2019,12,10)
    yyyymmdd = date.strftime("%Y%m%d")
    dir1 = rootdir + "/" + date.strftime("Y%Y/M%m/D%d")
    ofilepath = dir1+'/GEOS5_orig_res_'+yyyymmdd+'.py3test2.nc'
    ret = combine_met_data( rootdir, date, ofilepath )

    time1 = datetime.now()

    print(" sucessful : ", ret)
    print(" time elapsed : ", time1-time0)

    print('End TEST')
