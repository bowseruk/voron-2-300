import json
import os
import subprocess

with open(f"{os.path.expanduser('~')}/voron-2-300/config/printer.json") as f:
    data = json.load(f)

print(data)