#!/bin/sh

## This script creates a new klipper - The first arguement should be the board referene

# Klipper folder
klipper="~/klipper"
# voron repo folder
voron="~/voron-2-300"
cd ${klipper}
# Clean up the klipper folder
make clean
# Use the config file for the board
if [ -r "${voron}/config/klipper/${1}.config" ]
then
cp "${voron}/config/klipper/${1}.config"
# Make the binary that is in use
make -j4
# Make the 
cp "${klipper}/out/klipper.bin" "${voron}/binaries/klipper/${1}.bin"
else
echo "No config file available"
fi