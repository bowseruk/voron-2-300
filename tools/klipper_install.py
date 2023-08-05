import json
import os
import subprocess

with open(f"{os.path.expanduser('~')}/voron-2-300/config/printer.json") as f:
    data = json.load(f)

for device in data:
    print(f"canbus flash {device['name']} at {device['canbus_uuid']}")
    if device["canbridge"]:
        print("usb flash")

