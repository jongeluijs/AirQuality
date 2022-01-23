#!/bin/bash

# Make sure we are in the folder of the scripts (github clone)
  cd $(dirname $0)

# We are going to store the resulting html-file in the 'Archive" folder
  rm *.html 2> /dev/null
  [[ -d Archive ]] || mkdir Archive

# Get the airquality-report from device
  reportFile="airquality-$(date --date="yesterday" +"%Y%m%d").html"
  scp -i ~/.ssh/airquality pi@192.168.68.105:/home/pi/GitHub/AirQuality/${reportFile} .

# send mail
  echo "Sending mail"
  mutt -a ${reportFile} -s $(basename ${reportFile} .html) -- cees@jongeluijs.nl <<END
echo $(date)
END

# mv result to Archive
  mv ${reportFile} Archive

