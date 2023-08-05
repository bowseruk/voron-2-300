#!/bin/sh

## This script runs when there is an update to klipper

#directories
voron="~/voron-2-300"

# Boards in use
boards=("octopus_pro_f429" "pitb" "sb2040")
for board in "${boards[@]}"
do
    cd "${voron}/"
    ./tools/klipper.sh $board
done