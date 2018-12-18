#! /usr/bin/env python
import numpy
import python_geos5_das_2x

inFileName = '/glade/scratch/fvitt/GEOS/Y2018/M12/D11/GEOS5_orig_res_20181211.nc'

outFileName = '/glade/scratch/fvitt/pytest_geos_2deg.nc'
newLats = 96
newLons = 144
ret = python_geos5_das_2x.regrid_met_data( newLats, newLons, inFileName, outFileName )
print "ret = ",ret

outFileName = '/glade/scratch/fvitt/pytest_geos_1deg.nc'
newLats = 192
newLons = 288
ret = python_geos5_das_2x.regrid_met_data( newLats, newLons, inFileName, outFileName )
print "ret = ",ret

