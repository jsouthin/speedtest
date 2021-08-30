#!/usr/bin/env bash

ts=`date +"%Y-%m-%d %H:%M:%S"`
ts=`date +"%Y-%m-%d %H:%M:%S"`
epoch=`date +%s`

install_dir="/home/pi/Projects/speedtest"
# change this is you want to install to a different location
logfile="/home/pi/Projects/speedtest/speedtest.log"
# change this if you want the results to go to a different file
python_dir="/home/pi/Projects/speedtest/speedtest_env/bin/"
# change this to reflect the location to the preferred python binary executable
# running which python3 may help

curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python - > tmp.$epoch
while read p; do echo "[${ts}] ${p}" >> ${logfile}; done < tmp.$epoch
rm tmp.$epoch
# this is the bit of code that actually does the speed test

${python_dir}/python3 ${install_dir}/speedtest.py
# this vizualizes the data into a chart and saves to a .png file

/usr/bin/sudo scp ${install_dir}/speedtest.png /var/www/html/
# This optionally copies the .pgn to the preferred location for web-server to be able to broadcast the file
# This will depend on the webserver and settings used