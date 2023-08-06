import json
import os
import shutil
import time
import subprocess

def update_katapult(name):
    # Check there is a config file
    if not os.path.exists(f"{os.path.expanduser('~')}/voron-2-300/config/katapult/{name}.config"):
        return False
    # copy the required config over any that exist
    shutil.copyfile(f"{os.path.expanduser('~')}/voron-2-300/config/katapult/{name}.config", f"{os.path.expanduser('~')}/katapult/.config")
    # Clean up the klipper folder
    subprocess.run(["make", "clean"], cwd=f"{os.path.expanduser('~')}/katapult")
    # Make the binary that is in use
    subprocess.run(["make", "-j4"], cwd=f"{os.path.expanduser('~')}/katapult")
    # Move the file made out
    shutil.copyfile(f"{os.path.expanduser('~')}/katapult/out/deployer.bin", f"{os.path.expanduser('~')}/voron-2-300/binaries/katapult/{name}_deployer.bin")
    shutil.copyfile(f"{os.path.expanduser('~')}/katapult/out/katapult.bin", f"{os.path.expanduser('~')}/voron-2-300/binaries/katapult/{name}.bin")
    return True

def update_klipper(name):
    # Check there is a config file
    if not os.path.exists(f"{os.path.expanduser('~')}/voron-2-300/config/klipper/{name}.config"):
        return False
    # copy the required config over any that exist
    shutil.copyfile(f"{os.path.expanduser('~')}/voron-2-300/config/klipper/{name}.config", f"{os.path.expanduser('~')}/klipper/.config")
    # Clean up the klipper folder
    subprocess.run(["make", "clean"], cwd=f"{os.path.expanduser('~')}/klipper")
    # Make the binary that is in use
    subprocess.run(["make", "-j4"], cwd=f"{os.path.expanduser('~')}/klipper")
    # Move the file made out
    shutil.copyfile(f"{os.path.expanduser('~')}/klipper/out/klipper.bin", f"{os.path.expanduser('~')}/voron-2-300/binaries/klipper/{name}.bin")
    return True

# This command flashes a device. If its a canbridge, it will flash the device into usb mode, then updated it.
def flash_canbus(uuid, payload, canbridge=False, maxTries=10):
    if not canbridge:
        # Flash canbus module
        print(f"canbus flash device at {uuid} with {payload}")
        print(["python3", f"{os.path.expanduser('~')}/katapult/scripts/flashtool.py", "-i", "can0", "-f", payload, "-u", uuid])
        # subprocess.run(["python3", f"{os.path.expanduser('~')}/katapult/scripts/flashtool.py", "-i", "can0", "-f", payload, "-u", uuid])
        return
    # Flash usb if it is a canbridge
    else:
        if os.path.exists("/dev/serial/by-id/"):
            startingDevices = set(os.listdir("/dev/serial/by-id/"))
        else:
            startingDevices = set()
        print(f"canbus message to enter bootloader to {uuid}")
        print(["python3", f"{os.path.expanduser('~')}/katapult/scripts/flashtool.py", "-i", "can0", "-r", "-u", uuid])
        # retry looking for device until timeout
        for i in range(maxTries):
                if os.path.exists("/dev/serial/by-id/"):
                    currentDevices = set(os.listdir("/dev/serial/by-id/"))
                    for device in currentDevices - startingDevices:
                        print(f"usb flash {device} with {payload}")
                        print(["python3", f"{os.path.expanduser('~')}/katapult/scripts/flashtool.py", "-f", payload, "-d", device])
                        # subprocess.run(["python3", f"{os.path.expanduser('~')}/katapult/scripts/flashtool.py", "-f", payload, "-d", device])
                    break
                else:
                    # Sleep and then retry to see if bridge comes up
                    time.sleep(10)

## This function opens a json
def main():
    with open(f"{os.path.expanduser('~')}/voron-2-300/config/printer.json") as f:
        data = json.load(f)

    for device in data:
        if device["auto_update_katapult"]:
            update_katapult(device['name'])
            flash_canbus(device['canbus_uuid'], f"{os.path.expanduser('~')}/voron-2-300/binaries/katapult/{device['name']}_deployer.bin", device['canbridge'], 10)
        if device["auto_update_klipper"]:
            update_klipper(device['name'])
            flash_canbus(device['canbus_uuid'], f"{os.path.expanduser('~')}/voron-2-300/binaries/klipper/{device['name']}.bin", device['canbridge'], 10)

if __name__ == "__main__":
    main()