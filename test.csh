#!/bin/csh
#
# download GEOS5.11 forecast files
#  get first day of forecast from H00 dir
#  get days 2-5 from H12 dir
#  get 1st hour of day 6 from H12 dir
# combine files into one netcdf file per day
# regrid to 1.9x2.5 and 0.5x0.6

cd /glade/scratch/tilmes/FORECASTS/GEOS5

#-------------------------------------------
#  nominal days per month
#-------------------------------------------
set day_mnth = (31 28 31 30 31 30 31 31 30 31 30 31)

set years = (0 0 0 0 0 0)
set mnths = (0 0 0 0 0 0)
set days  = (0 0 0 0 0 0)

set n1 = 1

#-------------------------------------------
#  set current date variables
#-------------------------------------------
set dates = `date`
set date_ymd = `cat /glade/scratch/tilmes/FORECASTS/date_ymd_analysis`
set yr = $date_ymd[1]
set mnth = $date_ymd[2]
set day = $date_ymd[3]
echo $yr $mnth $day

set day_lim = 6

echo " "
echo "$0 begins execution on $dates"
echo "month = $mnth"
echo "day   = $day"
echo "year  = $yr"

#-------------------------------------------
#  leap year?
#-------------------------------------------
set lyr = yr
@ lyr = $yr % 4
if( $lyr == 0 ) then
  echo "$yr is a leap year: adjusting days in Feb"
  @ day_mnth[2]++
  echo $day_mnth
endif

echo " "
echo "today is $yr$mnth$day"
echo " "

set years[$n1] = $yr
set mnths[$n1] = $mnth
set days[$n1]  = $day

#-------------------------------------------
#  check input, output filepaths
#  create directories if required
#-------------------------------------------
foreach flnm (orig nc_orig_res 05x06 1.9x2.5)
  switch( $flnm )
    case orig:
      set flsp = "/glade/scratch/tilmes/GEOSfcst/$flnm/$years[$n1]/$mnths[$n1]/$days[$n1]"
      set geos5_dir = $flsp
      breaksw
    case nc_orig_res:
      set flsp = "/glade/scratch/tilmes/GEOSfcst/$flnm/$years[$n1]/$mnths[$n1]/$days[$n1]"
      breaksw
    case 05x06:
      set flsp = "/glade/scratch/tilmes/GEOSfcst/$flnm/$years[$n1]/$mnths[$n1]/$days[$n1]"
      breaksw
    case 1.9x2.5:
      set flsp = "/glade/scratch/tilmes/GEOSfcst/$flnm/$years[$n1]/$mnths[$n1]/$days[$n1]"
  endsw
  if( -d $flsp ) then
    echo "directory $flsp exists"
  else
    echo "directory $flsp does not exist"
    mkdir -p $flsp
    if( $status ) then
      echo "failed to create directory $flsp"
      exit -1
    else
      echo "created directory $flsp"
    endif
  endif
end

#-------------------------------------------
#  create date array
#-------------------------------------------
set pmnth = $mnth
set day_lst = (1 2 3 4 5)
echo "day list = $day_lst"

set day1 = $day
if ($day == 08) then
  set day1 = 8
endif
if ($day == 09) then
  set day1 = 9
endif
echo $day1

foreach n ($day_lst)
    set nday = $day1
    @ nday = $nday + $n
    @ nday = ($nday - 1) % $day_mnth[$pmnth] + 1

    if( $nday == 1 ) then
      set nmnth = $mnth
      if ($nmnth == 08) then
        set nmnth = 8
      endif
      if ($nmnth == 09) then
        set nmnth = 9
      endif
      @ nmnth = $nmnth % 12
      @ nmnth++
      if( $nmnth == 1 ) then
        @ yr++
      endif
      set mnth = $nmnth
      if( $mnth < 10 ) then
        set mnth = 0$mnth
      endif
    endif
    if( $nday < 10 ) then
      set nday = 0$nday
    endif
    @ n1++
    set years[$n1] = $yr
    set mnths[$n1] = $mnth
    set days[$n1]  = $nday
    echo "date for day $n is $years[$n1]$mnths[$n1]$days[$n1]"
end


# download files using lftp
set user = gmao_ops
set password = ""
set server = ftp.nccs.nasa.gov
set set_cmds = "set ftp:list-empty-ok true; set cmd:fail-exit true; set net:max-retries 5"
echo "local dir = $geos5_dir"

set sleep_dt = 900
set all_stop = 0
set n1 = 1

# get 1st day from H00
set remote_dir = /fp/forecast/Y$years[$n1]/M$mnths[$n1]/D$days[$n1]/H00
echo "remote dir = $remote_dir"
set fcst_date = $years[$n1]$mnths[$n1]$days[$n1]
echo $fcst_date

set loop_cnt = 0
set loop_lim = 12
set file_tot = 80

#while ( $loop_cnt < $loop_lim )
    echo $loop_cnt
    date
    set glob = "GEOS.fp.fcst.inst3_3d_asm_Nv*+"${fcst_date}"_*"
    echo " /usr/bin/lftp -c ${set_cmds}; open -u $user,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $geos5_dir "

    set glob = "GEOS.fp.fcst.tavg1_2d_flx_Nx*+"${fcst_date}"_*"
    echo " /usr/bin/lftp -c ${set_cmds}; open -u $user,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $geos5_dir"

    set glob = "GEOS.fp.fcst.tavg1_2d_lnd_Nx*+"${fcst_date}"_*"
    echo " /usr/bin/lftp -c ${set_cmds}; open -u $user,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $geos5_dir"

    set glob = "GEOS.fp.fcst.tavg1_2d_rad_Nx*+"${fcst_date}"_*"
    echo " /usr/bin/lftp -c ${set_cmds}; open -u $user,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $geos5_dir"

#    set xfer_file_cnt = `ls $geos5_dir/*+${fcst_date}_* | wc -l`
#    echo ${xfer_file_cnt} 
#    if( $xfer_file_cnt == $file_tot ) then
#      echo "Acquired $xfer_file_cnt H00 files"
#      date
#      break
#    endif
#    sleep $sleep_dt
#    @ loop_cnt++
#end

exit 0

set day_lst = (2 3 4 5 6)
echo "day list = $day_lst"
set n1 = 1
set remote_dir = /fp/forecast/Y$years[$n1]/M$mnths[$n1]/D$days[$n1]/H12
echo "remote dir = $remote_dir"
foreach n ($day_lst)
  set fcst_date = $years[$n]$mnths[$n]$days[$n]
  echo "fcst_date = $fcst_date"
  if( $n != $day_lim ) then
   set loop_cnt = 0
   set loop_lim = 12
   set file_tot = 80
   while ( $loop_cnt < $loop_lim )
    echo $loop_cnt
    date

    set glob = "GEOS.fp.fcst.inst3_3d_asm_Nv*+"${fcst_date}"_*"
    /usr/bin/lftp -c "${set_cmds}; open -u $user,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $geos5_dir"

    set glob = "GEOS.fp.fcst.tavg1_2d_flx_Nx.*+"${fcst_date}"_*"
    /usr/bin/lftp -c "${set_cmds}; open -u $user,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $geos5_dir"

    set glob = "GEOS.fp.fcst.tavg1_2d_lnd_Nx.*+"${fcst_date}"_*"
    /usr/bin/lftp -c "${set_cmds}; open -u $user,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $geos5_dir"

    set glob = "GEOS.fp.fcst.tavg1_2d_rad_Nx.*+"${fcst_date}"_*"
    /usr/bin/lftp -c "${set_cmds}; open -u $user,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $geos5_dir"

    set xfer_file_cnt = `ls $geos5_dir/*+${fcst_date}_* | wc -l`
    echo ${xfer_file_cnt} 
    if( $xfer_file_cnt == $file_tot ) then
      echo "Acquired $xfer_file_cnt H12 files for ${fcst_date}"
      date
      break
    endif
    sleep $sleep_dt
    @ loop_cnt++
   end
   if( $loop_cnt >= $loop_lim && $xfer_file_cnt == 0 ) then
      echo "There is a problem with the file transfer;  $0 is terminating"
      set all_stop = 1
      break
   endif

  else
    #get 00z of 6th day
    date
    set glob = "GEOS.fp.fcst.inst3_3d_asm_Nv*+"${fcst_date}"_00*"
    /usr/bin/lftp -c "${set_cmds}; open -u $user,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $geos5_dir"

    set glob = "GEOS.fp.fcst.tavg1_2d_flx_Nx.*+"${fcst_date}"_00*"
    /usr/bin/lftp -c "${set_cmds}; open -u $user,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $geos5_dir"

    set glob = "GEOS.fp.fcst.tavg1_2d_lnd_Nx.*+"${fcst_date}"_00*"
    /usr/bin/lftp -c "${set_cmds}; open -u $user,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $geos5_dir"

    set glob = "GEOS.fp.fcst.tavg1_2d_rad_Nx.*+"${fcst_date}"_00*"
    /usr/bin/lftp -c "${set_cmds}; open -u $user,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $geos5_dir"
    date
  endif
end

set dates = `date`
echo "$0 acquired files on $dates"


exit 0


#email dir listing 
set filecnt = `ls  $geos5_dir/*nc4 | wc -l`
set filelst = `ls  $geos5_dir/*nc4` 
set fname = 'list_download.txt'
echo "$filelst" > $fname
echo "." >> $fname
/bin/mailx -s "GEOS5.11 ftp count $filecnt" tilmes@ucar.edu 

#-------------------------------------------
#  check for failed transfer
#-------------------------------------------
if( $all_stop == 1 ) then
  echo "GEOS5.11 files not available."
  /bin/mailx -s "problem with GEOS5.11 download" tilmes@ucar.edu 
  exit
endif
exit

#-------------------------------------------
#  combine files to 1 netcdf file per day
#-------------------------------------------
set oflnm = geosfcst.idl.out
if( -e $oflnm ) then
  rm -f $oflnm
endif
date
idl run_combine_geosfcst >& $oflnm

# check dates in new files
set file_list = `ls /data/emmons/GEOSfcst/nc_orig_res/$years[$n1]/$mnths[$n1]/$days[$n1]/*.nc`
set fno = 1
set problem = 0

while ( $fno <= 5 )
 set hist_file = $file_list[$fno]
 echo $hist_file
 set nchar = `ls $hist_file | wc -m`
 @ c1 = $nchar - 11
 @ c2 = $c1 + 7
 set fdate = `echo $hist_file | cut -c$c1-$c2 `
 set date_line = `/usr/bin/ncdump -v date $hist_file |grep 'date = ' |sed 's/,//g'`
 echo "$date_line[3] $fdate"
 if ($date_line[3] != $fdate) then
    echo "$date_line[3] does not match $fdate"
    set problem = 1
    break
 endif
 @ fno = $fno + 1
end

# if at least one date in created files is bad, run IDL program again
if ($problem == 1) then
  idl run_combine_geosfcst >& $oflnm
endif

set dates = `date`
echo "$0 finished idl processing on $dates"
#/bin/mailx -s "geosfcst combine result" emmons@ucar.edu < "$oflnm"

#-------------------------------------------
#  setup regrid parameter file and run regridder
#-------------------------------------------
#foreach h_res (05x06 1.9x2.5)
foreach h_res (1.9x2.5 05x06)
  set iflnm = regrid.511.${h_res}.nml
  if( -e $iflnm ) then
    rm -f $iflnm
  endif
  echo "&CONTROLS" > $iflnm
  echo "start_year = $years[$n1]" >> $iflnm
  echo "start_mnth = $mnths[$n1]" >> $iflnm
  echo "start_day  = $days[$n1]" >> $iflnm
  echo "day_cnt    = $day_lim" >> $iflnm
  echo "hor_res    = '$h_res'" >> $iflnm
  echo "path_in    = '/data/emmons/GEOSfcst/nc_orig_res'" >> $iflnm
  echo "path_out   = '/data/emmons/GEOSfcst/$h_res'" >> $iflnm
  echo "/" >> $iflnm
  set oflnm = regrid.511.${h_res}.out
  if( -e $oflnm ) then
    rm -f $oflnm
  endif
  /home/emmons/GEOS5/forecasts/src_regrid_511/regrid_geos5.exe < $iflnm >& $oflnm
end

/bin/mailx -s "geos511 regridding complete" emmons@ucar.edu

echo " "
set dates = `date`
echo "$0 completed execution on $dates"

exit 0
