#!/bin/sh
##################################
## Run startup scripts, check if user is running Vagrant, launch.
##################################

# Make sure we have user variables defined, even if unset.
if [ -z "$USER" ]; then
  export USER="undefined"
fi

# Run gulp
echo " "
echo "%% Running Gulp . . ."
echo "========================================"
gulp scripts && gulp sass

if [ "$USER" = "vagrant" ]; then
  # May come in useful
  export VAGRANT_DEBUG="1"

  # Launch and bind to all network interfaces for Vagrant.
  echo " "
  echo "%% Launching with Vagrant bindings . . ."
  echo "========================================"
  dev_appserver.py --host=0.0.0.0 --port=8080 .
else
  echo " "
  echo "%% Launching dev server . . ."
  echo "========================================"
  dev_appserver.py --port=8080 .
fi

