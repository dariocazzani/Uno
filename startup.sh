#!/bin/sh

# activate environment variables
source ~/.profile_Uno

# change to bare repo
cd /home/pi/Dev/Uno.git

# set environment variable to version
export UNO_VERSION="$(git rev-parse HEAD | cut -c 1-10)"

# install requirements
cd /home/pi/Dev/Uno

pip install --user -r requirements.txt

# cd out of repo
cd /home/pi

# activate virtualenv
workon bots

# send IP to admin

# start services
cd /home/pi/Dev
python start.Ãpy
