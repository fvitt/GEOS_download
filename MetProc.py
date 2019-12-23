#! /usr/bin/env python
from datetime import datetime, timedelta
from os import path, remove, system
from subprocess import call
from glob import glob
from combine_met_data_eff import combine_met_data
from python_geos5_das_2x import regrid_met_data
from check_met_data import check_met_data

# untility object class for processing meteorolgy data 
class MetProc:

    def __init__( self, date, rootdir ):

        yyyymmdd = date.strftime("%Y%m%d")

        self.date = date
        self.rootdir = rootdir
        self.directory = self.rootdir + "/" + date.strftime("Y%Y/M%m/D%d")
        self.combined_data_filebase = 'GEOS5_orig_res_'+yyyymmdd+'.nc'

        if date.year < 2014 :
            self.regridded_data_filebase = 'GEOS5.7.2_19x2_'+yyyymmdd+'.nc'
            self.regridded_data_filebase_1deg = 'GEOS5.7.2_09x125_'+yyyymmdd+'.nc'
        else:
            self.regridded_data_filebase = 'GEOS5_19x2_'+yyyymmdd+'.nc'
            self.regridded_data_filebase_1deg = 'GEOS5_09x125_'+yyyymmdd+'.nc'

#        print 'self.regridded_data_filebase = ',self.regridded_data_filebase
#        print 'self.regridded_data_filebase_1deg = ',self.regridded_data_filebase_1deg
#
#        self.regridded_data_filebase = 'GEOS5.11.0_19x2_'+yyyymmdd+'.nc'
        self.combined_data_file = self.directory + '/' + self.combined_data_filebase
        self.regridded_data_file = self.directory +  '/' + self.regridded_data_filebase
        self.regridded_data_file_1deg = self.directory +  '/' + self.regridded_data_filebase_1deg

    def check( self, status ) :
        filepath = self.directory + "/."+status
        return path.exists(filepath)

    def download( self ): 
        year  = self.date.strftime("%Y")
        month = self.date.strftime("%m")
        day   = self.date.strftime("%d")
        cmd = ["./download_data","-year",year,"-month",month,"-day",day,'-local_basedir',self.rootdir]
        print " cmd: ",cmd
        stat = call(cmd)
        if stat == 0 :
            cmd = ['touch',self.directory+'/.downloaded']
            stat = call(cmd)
            return True
        else : 
            return False

    def combine( self ):
        #help(self.rootdir)
        sucessful = combine_met_data( self.rootdir, self.date, self.combined_data_file )
        if sucessful : 
            cmd = ['touch',self.directory+'/.combined']
            stat = call(cmd)
            sucessful = stat == 0
        return sucessful

    def regrid( self ):
        inFileName = self.combined_data_file
        outFileName = self.regridded_data_file
        newLats = 96
        newLons = 144
        stat = regrid_met_data( newLats, newLons, inFileName, outFileName )
        if stat == 0 : 
            cmd = ['touch',self.directory+'/.regridded']
            stat = call(cmd)
            if stat == 0 :
                return True
        return False

    def regrid_1deg( self ):
        inFileName = self.combined_data_file
        outFileName = self.regridded_data_file_1deg
        newLats = 192
        newLons = 288
        stat = regrid_met_data( newLats, newLons, inFileName, outFileName )
        if stat == 0 : 
            cmd = ['touch',self.directory+'/.regridded_1deg']
            stat = call(cmd)
            if stat == 0 :
                return True
        return False

    def validate( self ):
        file_ok = check_met_data( self.regridded_data_file )
        if file_ok:
            cmd = ['touch',self.directory+'/.validated']
            stat = call(cmd)      
            if stat == 0 :
                return True
        return file_ok 

    def validate_1deg( self ):
        file_ok = check_met_data( self.regridded_data_file_1deg )
        if file_ok:
            cmd = ['touch',self.directory+'/.validated_1deg']
            stat = call(cmd)      
            if stat == 0 :
                return True
        return file_ok 

    def archive(self):
        yyyy = self.date.strftime("%Y")

        lcldir = '/glade/p/cesm/chwg_dev/met_data/GEOS5/'+yyyy
        msdiro = '/CCSM/csm/met_data/GEOS5/orig_res/'+yyyy
        msdir2 = '/CCSM/csm/met_data/GEOS5/1.9x2.5/'+yyyy
        lcldir_1deg = '/glade/p/cesm/chwg_dev/met_data/GEOS5/0.9x1.25/'+yyyy
        msdir2_1deg = '/CCSM/csm/met_data/GEOS5/0.9x1.25/'+yyyy

        cmd = ['mkdir','-p',lcldir]
        stat = call(cmd)
        if not stat == 0 : return False
        cmd = ['cp',self.regridded_data_file,lcldir]
        stat = call(cmd)
        if not stat == 0 : return False

        cmd = ['mkdir','-p',lcldir_1deg]
        stat = call(cmd)
        if not stat == 0 : return False
        cmd = ['cp',self.regridded_data_file_1deg,lcldir_1deg]
        stat = call(cmd)
        if not stat == 0 : return False



        cmd = '/ncar/opt/hpss/hpss/bin/hsi -a P93300043 -q "mkdir -p '+msdiro+'"'
        print 'cmd = '+cmd
        stat = system(cmd)
        if not stat == 0 : return False
        cmd = '/ncar/opt/hpss/hpss/bin/hsi -a P93300043 -q "cd '+msdiro+' ; put '+self.combined_data_file + ' : '+ self.combined_data_filebase + ' ; chmod +r '+ self.combined_data_filebase +'"'
        print 'cmd = '+cmd
        stat = system(cmd)
        if not stat == 0 : return False

        cmd = '/ncar/opt/hpss/hpss/bin/hsi -a P93300043 -q "mkdir -p '+msdir2+'"'
        stat = system(cmd)
        if not stat == 0 : return False
        cmd = '/ncar/opt/hpss/hpss/bin/hsi -a P93300043 -q "cd '+msdir2+' ; put '+self.regridded_data_file + ' : '+ self.regridded_data_filebase + ' ; chmod +r '+ self.regridded_data_filebase +'"'
        print 'cmd = '+cmd
        stat = system(cmd)
        if not stat == 0 : return False



        cmd = '/ncar/opt/hpss/hpss/bin/hsi -a P93300043 -q "mkdir -p '+msdir2_1deg+'"'
        stat = system(cmd)
        if not stat == 0 : return False
        cmd = '/ncar/opt/hpss/hpss/bin/hsi -a P93300043 -q "cd '+msdir2_1deg+' ; put '+self.regridded_data_file_1deg + ' : '+ self.regridded_data_filebase_1deg + ' ; chmod +r '+ self.regridded_data_filebase_1deg +'"'
        print 'cmd = '+cmd
        stat = system(cmd)
        if not stat == 0 : return False

        cmd = ['touch',self.directory+'/.archived']
        stat = call(cmd)
        if not stat == 0 : return False

        return True

    def cleanup( self ) :
        if path.exists(self.directory):
            print " clean up dir : "+self.directory
            files = glob(self.directory+'/*.nc4') + glob(self.directory+'/*.nc')
            for f in files :
                print " try to rm : "+f
                stat = remove( f )
        return True

# unit test ...
def _test():
    # some test code:

    time0 = datetime.now()

    print "Begin Test"

#    date =  datetime(2013,12,31)
    date =  datetime(2019,7,11)

    geosproc = MetProc(date, '/glade/scratch/fvitt/GEOS_test')
    print "  check for : " + date.strftime("%x")

    downloaded = geosproc.check( 'downloaded' )
    print "Downloaded: ", downloaded

    if not downloaded :
        dwnld_ok = geosproc.download( )
        print " dwnld_ok = ",dwnld_ok

    time1 = datetime.now()

    combined = geosproc.check( 'combined')
    print "Combined: ",combined

    if not combined :
        combnd_ok = geosproc.combine( )
        print "combnd_ok: ",combnd_ok

    time2 = datetime.now()

    regridded = geosproc.check( 'regridded')
    print "Regridded: ",regridded

    if not regridded :
        regrd_ok = geosproc.regrid( )
        print "regd_ok: ",regrd_ok

    regridded_1deg = geosproc.check( 'regridded_1deg')
    print "Regridded 1deg: ",regridded_1deg

    if not regridded_1deg :
        regrd_ok = geosproc.regrid_1deg( )
        print "1deg regd_ok: ",regrd_ok

    time3 = datetime.now()

    data_ok = geosproc.validate()
    print "data_ok: ", data_ok
    if not data_ok: return False

    data_ok_1deg = geosproc.validate_1deg()
    print "data_ok_1deg: ", data_ok_1deg
    if not data_ok_1deg: return False

    time4 = datetime.now()

    archived = geosproc.check( 'archived')
    print "Archived: ", archived

    if not archived :
        arch_ok = geosproc.archive( )
        print "arch_ok: ",arch_ok

    time5 = datetime.now()

    print "Download time  : ", time1-time0
    print "Combine time   : ", time2-time1
    print "Regrid time    : ", time3-time2
    print "Data check time: ", time4-time3
    print "Archive time   : ", time5-time4
    print "Total time     : ", time5-time0

    print "Test Done"

