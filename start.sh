#!/bin/bash

# Template our config file
python3 /opt/config-generator.py >> /usr/local/apache2/conf/proxy.conf
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start config-generator.py: $status"
  exit $status
fi

# Start the first process
httpd -DFOREGROUND &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start httpd: $status"
  exit $status
fi

# Start the second process
python3 /opt/monitoring.py &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start monitoring.py: $status"
  exit $status
fi

# Naive check runs checks once a minute to see if either of the processes exited.
# This illustrates part of the heavy lifting you need to do if you want to run
# more than one service in a container. The container exits with an error
# if it detects that either of the processes has exited.
# Otherwise it loops forever, waking up every 60 seconds

while sleep 60; do
  ps aux |grep httpd |grep -q -v grep
  PROCESS_1_STATUS=$?
  ps aux |grep monitoring |grep -q -v grep
  PROCESS_2_STATUS=$?
  # If the greps above find anything, they exit with 0 status
  # If they are not both 0, then something is wrong
  if [ $PROCESS_1_STATUS -ne 0 -o $PROCESS_2_STATUS -ne 0 ]; then
    echo "One of the processes has already exited."
    exit 1
  fi
done
