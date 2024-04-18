#!/bin/bash

# Ensure the script is running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

# Create user 'ito' if it doesn't already exist
if ! id -u ito > /dev/null 2>&1; then
    useradd -m -s /bin/bash ito
fi

# Commands to run as the new 'ito' user
su ito <<'EOF'
cd ~
# Clone the repository into 'live' directory
git clone https://github.com/briandeheus/ito live

# Change directory to 'live'
cd live

# Create a Python virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Exit the virtual environment
deactivate

EOF

# Create a symlink for the systemd service
ln -sf /home/ito/live/.files/ito.service /etc/systemd/system/ito.service

# Reload systemd to recognize the new service
systemctl daemon-reload