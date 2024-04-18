#!/bin/bash

# Ensure the script is running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

# Switch to 'ito' user to fetch latest updates from the git repository
su ito -c 'cd ~/live && git pull origin main'

# Reload the systemd daemon
systemctl daemon-reload

# Restart the 'ito' service
systemctl restart ito.service