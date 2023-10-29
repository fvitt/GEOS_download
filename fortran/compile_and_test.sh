#!/bin/tcsh
#
#PBS -N compile_and_test
#PBS -A P19010000
#PBS -l select=1:ncpus=1:mem=100GB
#PBS -l walltime=00:40:00
#PBS -q casper
#PBS -j oe

module purge
module load ncarenv
module load ncarbinlibs
module load intel
module load ncarcompilers
module load netcdf
module load conda
module list

conda activate npl

f2py -c  --compiler=intelem --fcompiler=intelem --f90flags="-132 -ftz -FR -O2" -L$NETCDF/lib -lnetcdf python_geos5_das_2x.f90 -m python_geos5_das_2x

test_python_geos5_das_2x.py
