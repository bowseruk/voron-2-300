#!/bin/sh

#directories
voron="~/voron-2-300"
katapult="~/katapult"

## This script installs klippeer updates using katapult

# Check if the binarie exists
if [ -r "${voron}/binaries/klipper/${1}.bin" ]
then
    # Flash the bridge in canbus then usb
    if [ ${1} == "octopus_pro_f429" ]
    then
        python3 "${katapult}/scripts/flashtool.py" -i can0 -f "${voron}/binaries/klipper/${1}.bin" -u ${2}
        sleep 30
        for board in /dev/serial/by-id/
        do
            python3 "${katapult}/scripts/flashtool.py" -f "${voron}/binaries/klipper/${1}.bin" -d ${board}
        done
else
    # All other flash directly
    python3 "${katapult}/scripts/flashtool.py" -i can0 -f "${voron}/binaries/klipper${1}" -u ${2}
fi

else
    echo "No binary found"
fi