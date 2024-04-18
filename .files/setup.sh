#!/bin/bash

# Create user 'ito'
useradd -m ito

# Switch to user 'ito'
su - ito <<EOF

# Clone the repository into the 'live' directory
git clone https://github.com/briandeheus/ito live

# Create a virtual environment in the 'live' directory
cd live
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate

EOF

# Exit user 'ito'
exit

# Make symlink for systemd service
ln -s /home/ito/live/.files/ito.service /etc/systemd/system/ito.service
