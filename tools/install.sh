#!/bin/sh

# This is the directory for this repo and then other used repos
repo="~/voron-2-300"
klipper="~/klipper"
katapult="~/katapult"
network="/etc/network/interfaces.d"
printerdata="~/printer_data"

# Setup the canbus network ready for the Octopus canbus bridge
cp "${repo}/network/can0" ${network}

# Setup the printer config files
cp "${repo}/printer_data/*" ${printerdata}