#!/bin/sh
##################################
## Run startup scripts, check if user is running Vagrant, launch.
##################################

# Run gulp
echo " "
echo "%% Running Gulp . . ."
echo "========================================"
gulp scripts && gulp sass

# If a .vagrant folder exists, assume we're inside of a Vagrant machine.
if [ -d \.vagrant ]; then
  # May come in useful
  export VAGRANT_DEBUG="1"

  # Launch and bind to all network interfaces for Vagrant.
  echo " "
  echo "%% Launching with Vagrant bindings . . ."
  echo "========================================"
  dev_appserver.py --host=0.0.0.0 --admin_host=0.0.0 --port=8080 --use_mtime_file_watcher=True .
else
  echo " "
  echo "%% Launching dev server . . ."
  echo "========================================"
  dev_appserver.py --port=8080 .
fi
