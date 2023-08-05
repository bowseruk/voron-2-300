import json
import subprocess

with open("~/voron-2-300/config/printer.json") as f:
    data = json.load(f)

print(data)