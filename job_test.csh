#!/bin/tcsh
#
# LSF batch script
#

#BSUB -W 00:05                # wall-clock time (hrs:mins)
#BSUB -n 1                    # number of tasks in job         
#BSUB -J job_test             # job name
#BSUB -o job_test.%J.out      # output file name in which %J is replaced by the job ID
#BSUB -e job_test.%J.out      # error file name in which %J is replaced by the job ID
#BSUB -q caldera              # queue
#BSUB -P P19010000

echo "Begin Job"

cd /glade/u/home/fvitt/mygeos_download

set next_run_time = `proc_script.py`

echo "bsub -b $next_run_time < job_test.csh"

bsub -b $next_run_time < job_test.csh 

echo "End Job"


exit 0
