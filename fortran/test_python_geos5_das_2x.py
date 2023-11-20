#! /usr/bin/env python
import numpy
import fortran_regrid

inFileName = '/glade/scratch/fvitt/GEOS/Y2023/M10/D09/GEOS5_orig_res_20231009.nc'

outFileName = '/glade/scratch/fvitt/pytest_geos_2deg.nc'
newLats = 96
newLons = 144
ret = fortran_regrid.regrid_met_data( newLats, newLons, inFileName, outFileName )
print("ret = ",ret)

outFileName = '/glade/scratch/fvitt/pytest_geos_1deg.nc'
newLats = 192
newLons = 288
ret = fortran_regrid.regrid_met_data( newLats, newLons, inFileName, outFileName )
print("ret = ",ret)
