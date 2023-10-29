#! /usr/bin/env python
import numpy
import python_geos5_das_2x

inFileName = '/glade/scratch/fvitt/GEOS/Y2023/M08/D01/GEOS5_orig_res_20230801.nc'

outFileName = '/glade/scratch/fvitt/pytest_geos_2deg.nc'
newLats = 96
newLons = 144
ret = python_geos5_das_2x.regrid_met_data( newLats, newLons, inFileName, outFileName )
print("ret = ",ret)

outFileName = '/glade/scratch/fvitt/pytest_geos_1deg.nc'
newLats = 192
newLons = 288
ret = python_geos5_das_2x.regrid_met_data( newLats, newLons, inFileName, outFileName )
print("ret = ",ret)
