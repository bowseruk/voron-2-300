import json
import os
import time
import subprocess

with open(f"{os.path.expanduser('~')}/voron-2-300/config/printer.json") as f:
    data = json.load(f)

for device in data:
    if device["canbridge"]:
        if os.path.exists("/dev/serial/by-id/"):
            startingDevices = set(os.listdir("/dev/serial/by-id/"))
        else:
            startingDevices = set()

    print(f"canbus flash {device['name']} at {device['canbus_uuid']}")
    if device["canbridge"]:
        for i in range(10):
            if os.path.exists("/dev/"):
                currentDevices = set(os.listdir("/dev/"))
                for device in currentDevices - startingDevices:
                    print(f"usb flash {device}")
                return
            else:
                time.sleep(10)

