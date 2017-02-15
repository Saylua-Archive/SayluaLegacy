#!/bin/sh
##################################
## Update dependencies, Run startup scripts, check if user is running Vagrant, launch.
##################################

if [ "$1" = "--skip" ]; then
  echo " "
  echo "%% Skipping Dependency Updates . . ."
  echo "========================================"
else

  # Update Node dependencies
  echo " "
  echo "%% Updating Node Dependencies . . ."
  echo "========================================"
  npm update --dev
  echo "Done."

  # Update Python dependencies
  echo " "
  echo "%% Updating Python Dependencies . . ."
  echo "========================================"
  pip install -r requirements.txt -t lib -q --cache-dir lib/cache
  echo "Done."

  # Run gulp
  echo " "
  echo "%% Running Gulp . . ."
  echo "========================================"
  gulp build
  echo "Done."
fi

# If a .vagrant folder exists, assume we're inside of a Vagrant machine.
if [ -d \.vagrant ]; then
  # May come in useful
  export VAGRANT_DEBUG="1"

  # Launch and bind to all network interfaces for Vagrant.
  echo " "
  echo "%% Launching with Vagrant bindings . . ."
  echo "========================================"
  dev_appserver.py --host=0.0.0.0 --admin_host=0.0.0.0 --port=8080 --use_mtime_file_watcher=True .
else
  echo " "
  echo "%% Launching dev server . . ."
  echo "========================================"
  dev_appserver.py --port=8080 .
fi
