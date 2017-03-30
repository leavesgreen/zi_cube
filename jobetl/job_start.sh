#!/bin/bash

today=$(date +%Y-%m-%d)' 00:00:00'
fromday=$(date --date='1 day ago' +%Y-%m-%d)' 00:00:00'
jobid=$(date +%Y%m%d)
batchid=$(date +%H%M%S)

echo $fromday
echo $today
echo $jobid
echo $batchid

cd /home/dev/myenv
source ./bin/activate
/home/dev/myenv/bin/python  /home/dev/myenv/pdi_jobs/shell_load_main_to_es/es_load_main_brand_dat.py  $fromday $today >> ./pdi_jobs/shell_load_main_to_es/run.log
deactivate
