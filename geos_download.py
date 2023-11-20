#! /usr/bin/env python
from datetime import datetime, timedelta
from subprocess import call

def download(date, rootdir) :

    dstdir = rootdir+'/'+date.strftime("Y%Y/M%m/D%d")
    url = 'https://portal.nccs.nasa.gov/datashare/gmao_ops/pub/fp/das/' + date.strftime("Y%Y/M%m/D%d") + '/'
    #print('url ',url)
    print('dstdir: ',dstdir)

    cmd = ['mkdir','-p',dstdir]
    stat = call(cmd)
    if (stat!=0) : return False

    datestr =  date.strftime("%Y%m%d")
    #print('datestr: ',datestr)

    stat = 0

    for t in range(0,25,3) :
        t1 = t-1
        t2 = t

        if (t1>0) :
            tstr = str(t1).zfill(2)
            sfx = datestr+'_'+tstr+'30'+'.V01.nc4'

            file = url+'GEOS.fp.asm.tavg1_2d_flx_Nx.'+sfx
            print(' get :',file)
            cmd = ['wget','-q','-c','-P',dstdir,file]
            stat = call(cmd)
            if (stat!=0) : return False

            file = url+'GEOS.fp.asm.tavg1_2d_lnd_Nx.'+sfx
            print(' get :',file)
            cmd = ['wget','-q','-c','-P',dstdir,file]
            stat = call(cmd)
            if (stat!=0) : return False

            file = url+'GEOS.fp.asm.tavg1_2d_rad_Nx.'+sfx
            print(' get :',file)
            cmd = ['wget','-q','-c','-P',dstdir,file]
            stat = call(cmd)
            if (stat!=0) : return False

        if (t2<24) :
            tstr = str(t2).zfill(2)
            sfx = datestr+'_'+tstr+'30'+'.V01.nc4'

            file = url+'GEOS.fp.asm.tavg1_2d_flx_Nx.'+sfx
            print(' get :',file)
            cmd = ['wget','-q','-c','-P',dstdir,file]
            stat = call(cmd)
            if (stat!=0) : return False

            file = url+'GEOS.fp.asm.tavg1_2d_lnd_Nx.'+sfx
            print(' get :',file)
            cmd = ['wget','-q','-c','-P',dstdir,file]
            stat = call(cmd)
            if (stat!=0) : return False

            file = url+'GEOS.fp.asm.tavg1_2d_rad_Nx.'+sfx
            print(' get :',file)
            cmd = ['wget','-q','-c','-P',dstdir,file]
            stat = call(cmd)
            if (stat!=0) : return False

        if (t<24):
            tstr = str(t).zfill(2)
            sfx = datestr+'_'+tstr+'00.V01.nc4'

            file =  url+'GEOS.fp.asm.inst3_3d_asm_Nv.'+sfx
            print(' get :',file)
            cmd = ['wget','-q','-c','-P',dstdir,file]
            stat = call(cmd)
            if (stat!=0) : return False

    return True

def _test() :

    print('Begin TEST')
    date = datetime(2023,10,10)

    time0 = datetime.now()

    ok = download(date,'/glade/scratch/fvitt/GEOS_test')

    time1 = datetime.now()

    print('success = ',ok)


    print("Download time  : ", time1-time0)

    print('End TEST')
