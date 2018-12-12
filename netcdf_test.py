#! /usr/bin/env python
import Nio
import os
import numpy
import glob

def write_inst_flds( vars, files, out_file ):

    for ivar in vars.keys():
        ovar = vars[ivar]
        print ivar+' --> '+ovar
        cnt = 0
        for fin in files:
            in_file = Nio.open_file(fin)
            if cnt == 0:
                type=in_file.variables[ivar].typecode()
                vdims=in_file.variables[ivar].dimensions
                out_file.create_variable(ovar,type,vdims)
                varatts = in_file.variables[ivar].__dict__.keys()
                for att in varatts:
                    val = getattr(in_file.variables[ivar],att)
                    setattr(out_file.variables[ovar],att,val)

            v = in_file.variables[ivar].get_value()
            ndims = in_file.variables[ivar].rank
            v = numpy.roll(v,nroll,axis=ndims-1)
            if cnt > 0 :
                val = numpy.append(val,v,axis=0)
            else :
                val = v

            cnt = cnt+1
            in_file.close()
        out_file.variables[ovar].assign_value(val)

def write_tavg_flds( vars, files, out_file ):

    for ivar in vars.keys():
        ovar = vars[ivar]
        print ivar+' --> '+ovar
        for n in range(1,24,3):
            print filepaths[n-1]
            print filepaths[n]

            filem = Nio.open_file(filepaths[n-1])
            filep = Nio.open_file(filepaths[n])
            if n == 1:
                type=filep.variables[ivar].typecode()
                vdims=filep.variables[ivar].dimensions
                out_file.create_variable(ovar,type,vdims)
                varatts = filep.variables[ivar].__dict__.keys()
                for att in varatts:
                    val = getattr(filep.variables[ivar],att)
                    setattr(out_file.variables[ovar],att,val)

            valm = filem.variables[ivar].get_value()
            valp = filep.variables[ivar].get_value()
            ndims = filep.variables[ivar].rank
            vala = valm+valp
            vala = 0.5*vala
            if ovar=='TAUX' or ovar=='TAUY' :
                vala = -vala
            if ovar=='ALB':
                vala[valm.mask] = vala.fill_value
                vala[valp.mask] = vala.fill_value
            vala = numpy.roll(vala,nroll,ndims-1)
            if n > 1 :
                val = numpy.append(val,vala,axis=0)
            else :
                val = vala
            filem.close()
            filep.close()

        out_file.variables[ovar].assign_value(val)



#
# Set the PreFill option to False to improve writing performance
#
opt = Nio.options()
opt.PreFill = False

#
# Options for writing NetCDF4 "classic" file.
#
# If Nio wasn't built with netcdf 4 support, you will get a
# warning here, and the code will use netcdf 3 instead.
#
opt.Format = "netcdf4classic"

cdf_file = Nio.open_file('/glade/p/work/tilmes/MET/MERRA/const/MERRA_1979_orig_res_19790101.nc',mode='r')

#lev  = cdf_file.variables["lev"]
#ilev = cdf_file.variables["ilev"]
#hyam = cdf_file.variables["hyam"]
#hyai = cdf_file.variables["hyai"]
#hybm = cdf_file.variables["hybm"]
#hybi = cdf_file.variables["hybi"]
#P0   = cdf_file.variables["P0"]

vars = ["lev","ilev","hyam","hybm","hyai","hybi"]

ofilepath = '/glade/scratch/fvitt/GEOS/Y2013/M11/D30/my_test_file.nc'
os.system("/bin/rm -f "+ofilepath)
out_file = Nio.open_file(ofilepath,mode='c')

length = cdf_file.dimensions["lev"]
out_file.create_dimension("lev",length)

length = cdf_file.dimensions["ilev"]
out_file.create_dimension("ilev",length)

for var in vars:
    type=cdf_file.variables[var].typecode()
    vdims=cdf_file.variables[var].dimensions
    out_file.create_variable(var,type,vdims)
    varatts = cdf_file.variables[var].__dict__.keys()
    for att in varatts:
        val = getattr(cdf_file.variables[var],att)
        setattr(out_file.variables[var],att,val)

# Write coordinate dimension variables first

for var in vars:
    if cdf_file.dimensions.keys().count(var) > 0:
        v = cdf_file.variables[var].get_value()
        out_file.variables[var].assign_value(v)
        print "finished writing " + var

for var in vars:
    if cdf_file.dimensions.keys().count(var) == 0:
        v = cdf_file.variables[var].get_value()
        out_file.variables[var].assign_value(v)
        print "finished writing " + var
            
#
cdf_file.close()

hrz_file = Nio.open_file('/glade/p/work/tilmes/MET/GEOS572/const/GEOS.fp.asm.const_2d_asm_Nx.00000000_0000.V01.nc4')

length = hrz_file.dimensions["lat"]
out_file.create_dimension("lat",length)

length = hrz_file.dimensions["lon"]
out_file.create_dimension("lon",length)

out_file.create_dimension("time",None)

vars = ["lon","lat","PHIS"]
for var in vars:
    type=hrz_file.variables[var].typecode()
    vdims=hrz_file.variables[var].dimensions
    out_file.create_variable(var,type,vdims)
    varatts = hrz_file.variables[var].__dict__.keys()
    for att in varatts:
        val = getattr(hrz_file.variables[var],att)
        setattr(out_file.variables[var],att,val)

#for var in vars:
#    if hrz_file.dimensions.keys().count(var) > 0:

var = "lat"
v = hrz_file.variables[var].get_value()
out_file.variables[var].assign_value(v)
print "finished writing " + var

var = "lon"
v = hrz_file.variables[var].get_value()
neglons = numpy.where(v<0.0)
nroll = neglons[0][-1]+1
lons = numpy.roll(v, nroll )
lons = numpy.where(lons<0., lons+360., lons)
lons = numpy.where(lons<1.e-3, 0., lons)
out_file.variables[var].assign_value(lons)

dims = ('time',)
out_file.create_variable("time",'d',dims)
times = [0, 180, 360, 540, 720, 900, 1080, 1260]
out_file.variables['time'].assign_value(times)

for var in vars:
    if hrz_file.dimensions.keys().count(var) == 0:
        v = hrz_file.variables[var].get_value()
        v = numpy.roll(v,nroll,axis=2)
        print v.shape
        v = numpy.tile(v,(8,1,1))
        print v.shape
        out_file.variables[var].assign_value(v)
        print "finished writing " + var
            

type=hrz_file.variables["FRLAND"].typecode()
vdims=hrz_file.variables["FRLAND"].dimensions
out_file.create_variable("ORO",type,vdims)
varatts = hrz_file.variables["FRLAND"].__dict__.keys()
for att in varatts:
    val = getattr(hrz_file.variables["FRLAND"],att)
    setattr(out_file.variables["ORO"],att,val)

print " "
print " ++++++++++++++++++++++++++++++++++++++++++++++++++++ "
print " "

filem = glob.glob('/glade/scratch/fvitt/GEOS/Y2013/M11/D29/GEOS.fp.asm.tavg1_2d_flx_Nx.*_2330.V01.nc4' )
files = glob.glob('/glade/scratch/fvitt/GEOS/Y2013/M11/D30/GEOS.fp.asm.tavg1_2d_flx_Nx.*.nc4')
files.sort()

filepaths = filem + files
vars = {'HFLUX':'SHFLX', 'TAUX':'TAUX','TAUY':'TAUY', 'EVAP':'QFLX'}

write_tavg_flds( vars, filepaths, out_file )

print " "
print " ++++++++++++++++++++++++++++++++++++++++++++++++++++ "
print " "

ivar = 'FRSEAICE'
for n in range(1,24,3):
    print filepaths[n-1]
    print filepaths[n]

    filem = Nio.open_file(filepaths[n-1])
    filep = Nio.open_file(filepaths[n])

    valm = filem.variables[ivar].get_value()
    valp = filep.variables[ivar].get_value()
    ndims = filep.variables[ivar].rank
    print valm.shape
    print valp.shape
    vala = 0.5*(valm+valp)
    vala = numpy.roll(vala,nroll,ndims-1)
    if n > 1 :
        val = numpy.append(val,vala,axis=0)
    else :
        val = vala

seaice = val

v = hrz_file.variables["FRLAND"].get_value()
v = numpy.roll(v,nroll,axis=2)
v = numpy.tile(v,(8,1,1))
v = numpy.where(v==2, 1, v)
v = numpy.where(seaice>0.5,2,v)
out_file.variables["ORO"].assign_value(v)
print "finished writing " + "ORO"

print " "
print " ++++++++++++++++++++++++++++++++++++++++++++++++++++ "
print " "

filem = glob.glob('/glade/scratch/fvitt/GEOS/Y2013/M11/D29/GEOS.fp.asm.tavg1_2d_rad_Nx.*_2330.V01.nc4' )
files = glob.glob('/glade/scratch/fvitt/GEOS/Y2013/M11/D30/GEOS.fp.asm.tavg1_2d_rad_Nx.*.nc4')
files.sort()

filepaths = filem + files
vars = {'ALBEDO':'ALB', 'TS':'TS', 'SWGDN':'FSDS'}

write_tavg_flds( vars, filepaths, out_file )


print " "
print " ++++++++++++++++++++++++++++++++++++++++++++++++++++ "
print " "

filem = glob.glob('/glade/scratch/fvitt/GEOS/Y2013/M11/D29/GEOS.fp.asm.tavg1_2d_lnd_Nx.*_2330.V01.nc4' )
files = glob.glob('/glade/scratch/fvitt/GEOS/Y2013/M11/D30/GEOS.fp.asm.tavg1_2d_lnd_Nx.*.nc4')
files.sort()

filepaths = filem + files
vars = {'GWETTOP':'SOILW', 'SNOMAS':'SNOWH'}

write_tavg_flds( vars, filepaths, out_file )


print " "
print " ++++++++++++++++++++++++++++++++++++++++++++++++++++ "
print " "
print " "
print " ++++++++++++++++++++++++++++++++++++++++++++++++++++ "
print " "
 
 
hrz_file.close()

# instantaneous fields ....
files = glob.glob('/glade/scratch/fvitt/GEOS/Y2013/M11/D30/GEOS.fp.asm.inst3_3d_asm_Nv.*.nc4')
files.sort()

vars = {'PS':'PS','T':'T','U':'U','V':'V','QV':'Q'}

write_inst_flds( vars, files, out_file )

print " "
print " ++++++++++++++++++++++++++++++++++++++++++++++++++++ "
print " "

out_file.close()



