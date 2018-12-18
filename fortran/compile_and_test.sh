#!/bin/tcsh
#
#SBATCH -J compile_and_test
#SBATCH -n 4
#SBATCH -N 1
#SBATCH -t 00:30:00
#SBATCH -p dav
#SBATCH -C skylake
#SBATCH -o compile_and_test.out.%J
#SBATCH -e compile_and_test.out.%J
#SBATCH --account=P19010000
#SBATCH --mem 50G

module purge
module load ncarenv
module load ncarbinlibs
module load intel
module load ncarcompilers
module load netcdf
module load python
module list
ncar_pylib

f2py -c  --compiler=intelem --fcompiler=intelem --f90flags="-132 -ftz -FR -O2" -L$NETCDF/lib -lnetcdf python_geos5_das_2x.f90 -m python_geos5_das_2x

test_python_geos5_das_2x.py

