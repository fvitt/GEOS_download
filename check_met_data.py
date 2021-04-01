#! /usr/bin/env python
import numpy as np
import xarray as xr

def check_var( ds, varname, minx, maxx ):
    minval = np.amin(ds[varname].values)
    maxval = np.amax(ds[varname].values)

    if  minval<minx or maxval>maxx :
        print(varname + "... minval = " + str(minval) + "   maxval = " + str(maxval))
        return False

    return True

def check_met_data( filepath ):

    ds = xr.open_dataset(filepath)
    ok = True

    if ok: ok = check_var ( ds, "T",  1.e1, 1.e3 )
    if ok: ok = check_var ( ds, "U", -1.e3, 1.e3 )
    if ok: ok = check_var ( ds, "V", -1.e3, 1.e3 )
    if ok: ok = check_var ( ds, "PS", 1.e3, 1.e6 )
    if ok: ok = check_var ( ds, "SHFLX", -1.e5, 3.e5 )
    if ok: ok = check_var ( ds, "PHIS", -2.e3, 1.e6 )
    if ok: ok = check_var ( ds, "QFLX", -1.e-3, 1.   )
    if ok: ok = check_var ( ds, "TAUX", -1.e2, 1.e2 )
    if ok: ok = check_var ( ds, "TAUY", -1.e2, 1.e2 )
    if ok: ok = check_var ( ds,  "ORO",    0., 2.   )

    ds.close()
    if not ok:
        print(" ***** UNREALISTIC VALUES FOUND IN: "+filepath)
    return ok

def _test():
    print('Begin Test ...')
    #filepath = '/glade/scratch/fvitt/GEOS/Y2019/M12/D10/GEOS5_19x2_20191210.nc'
    filepath = '/glade/scratch/fvitt/GEOS_test/Y2019/M12/D10/GEOS5_orig_res_20191210.py3test2.nc'
    print("check file: ",filepath)
    ok = check_met_data( filepath )

    print("file ok : ",ok)

    print('End Test ...')
