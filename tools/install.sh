#!/bin/sh

# This is the directory for this repo and then other used repos
repo="~/voron-2-300"
klipper="~/klipper"
katapult="~/katapult"
network="/etc/network/interfaces.d"
printerdata="~/printer_data"

# Setup the canbus network ready for the Octopus canbus bridge
cp "${repo}/network/*" ${network}

# Get a placeholder to make a unique folder
backupfolder=$(date +%Y%m%d_%H%M%S)

# Dump current contents of config and copy the linked printer.cfg
mkdir "${repo}/config/backup/${backupfolder}"
cp "${printerdata}/config/*" "${repo}/config/backup/${backupfolder}"

# Setup the printer config files
cp "${repo}/printer_data/install/printer.cfg" "${printerdata}/config"