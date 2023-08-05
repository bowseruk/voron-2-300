import json
import os
import time
import subprocess

# This command flashes a device. If its a canbridge, it will flash the device into usb mode, then updated it.
def flash_canbus(uuid, payload, canbridge=False, maxTries=10):
    if canbridge:
        # IF there are any serial devices, log them so they won't be flashed.
        if os.path.exists("/dev/serial/by-id/"):
            startingDevices = set(os.listdir("/dev/serial/by-id/"))
        else:
            startingDevices = set()
    # Flash canbus module
    print(f"canbus flash device at {uuid} with {payload}")
    # Flash usb if it is a canbridge
    if canbridge:
        # retry looking for device until timeout
        for i in range(maxTries):
                if os.path.exists("/dev/"):
                    currentDevices = set(os.listdir("/dev/"))
                    for device in currentDevices - startingDevices:
                        print(f"usb flash {device} with {payload}")
                    break
                else:
                    # Sleep and then retry to see if bridge comes up
                    time.sleep(10)

## This function opens a json
def main():
    with open(f"{os.path.expanduser('~')}/voron-2-300/config/printer.json") as f:
        data = json.load(f)

    for device in data:
        flash_canbus(device['canbus_uuid'], device['name'], device['canbus_canbridge'], 10)

if __name__ == "__main__":
    main()