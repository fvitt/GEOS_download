#!/bin/csh

echo "BEGIN TEST"

set argnum = 0

set ftpuser = "gmao_ops"
set password = ""
set server = ftp.nccs.nasa.gov

set base_filename = "GEOS.fp.asm"
set remote_basedir = "/fp/das"
set local_basedir = "/glade/scratch/$USER/GEOS"

set ftpuser = "gmao_ops"
set password = ""
set server = ftp.nccs.nasa.gov

#ftp://gmao_ops@ftp.nccs.nasa.gov/fp/das/Y2013/M11/D18/GEOS.fp.asm.inst1_2d_smp_Nx.20131118_1900.V01.nc4

#set year = "unset"

foreach arg ($argv)
  @ argnum++
  @ argnump = $argnum + 1
  switch ($arg)
   case "-year":
     set year = "$argv[$argnump]"; breaksw
   case "-month":
     set month = "$argv[$argnump]"; breaksw
   case "-day":
     set day = "$argv[$argnump]"; breaksw
   case "-hour":
     set hour = "$argv[$argnump]"; breaksw
   case "-remote_basedir":
     set remote_basedir = "$argv[$argnump]"; breaksw
   case "-local_basedir":
     set local_basedir = "$argv[$argnump]"; breaksw
   case "-base_filename":
     set base_filename = "$argv[$argnump]"; breaksw
  endsw

end

set yyyymmdd_date = ${year}${month}${day}

echo "yyyymmdd_date = $yyyymmdd_date"

set local_dir = "${local_basedir}/Y${year}/M${month}/D${day}"
set remote_dir = "${remote_basedir}/Y${year}/M${month}/D${day}"
if (${?hour}) then
  set remote_dir = "${remote_dir}/H${hour}"
  set local_dir = "${local_dir}/H${hour}"
endif

echo "remote_dir = $remote_dir"
echo "local_dir = $local_dir"

set set_cmds = "set ftp:list-empty-ok true; set cmd:fail-exit true; set net:max-retries 5"

set loop_cnt = 0
set loop_lim = 12
set file_tot = 80
set sleep_dt = 900

echo "mkdir -p $local_dir"
mkdir -p $local_dir

while ( $loop_cnt < $loop_lim )
    echo "loop_cnt = $loop_cnt"
    date
    set glob = "${base_filename}.inst3_3d_asm_Nv*"
    echo " /usr/bin/lftp -c ${set_cmds}; open -u $ftpuser,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $local_dir"
    /usr/bin/lftp -c "${set_cmds}; open -u $ftpuser,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $local_dir"

    set glob = "${base_filename}.tavg1_2d_flx_Nx*"
    echo " /usr/bin/lftp -c ${set_cmds}; open -u $ftpuser,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $local_dir"
    /usr/bin/lftp -c "${set_cmds}; open -u $ftpuser,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $local_dir"

    set glob = "${base_filename}.tavg1_2d_lnd_Nx*"
    echo " /usr/bin/lftp -c ${set_cmds}; open -u $ftpuser,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $local_dir"
    /usr/bin/lftp -c "${set_cmds}; open -u $ftpuser,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $local_dir"

    set glob = "${base_filename}.tavg1_2d_rad_Nx*"
    echo " /usr/bin/lftp -c ${set_cmds}; open -u $ftpuser,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $local_dir"
    /usr/bin/lftp -c "${set_cmds}; open -u $ftpuser,$password $server; mirror -r -p --parallel=4 --no-symlinks -L --verbose=1 -I $glob $remote_dir $local_dir"

    date

    echo "ls $local_dir/*${yyyymmdd_date}_* "
    set xfer_file_cnt = `ls $local_dir/*${yyyymmdd_date}_* | wc -l`
    echo ${xfer_file_cnt} 
    if( $xfer_file_cnt == $file_tot ) then
      echo "Acquired $xfer_file_cnt files"
      exit 0
    endif
    sleep $sleep_dt
    @ loop_cnt++
end

echo "END TEST"
