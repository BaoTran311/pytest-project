# !/usr/bin/python3
import optparse
import subprocess

import yaml

from apps.consts import ENV_FILE

parser = optparse.OptionParser(usage="%prog [-d][-i]", version="%prog 1.0.0")
parser.add_option("-m", "--main", action="store_true", default=False)
parser.add_option("-p", "--platforms", help="Platforms that verify synchronizes data")
parser.add_option("-e", "--env", help="Environment file")
parser.add_option("-s", "--slot", type=int, default=1, help="The slot index for a certain connected device")
(option, args) = parser.parse_args()
platform_name = option.platforms
platform_slot = option.slot
device_uid, browser_name = (None,) * 2

if platform_name.lower() in ("chrome", "firefox"):
    browser_name = platform_name.lower()
    platform_name = "web"
    print(f"browser: {browser_name}")

command = f"ios-deploy -c -W | grep -i ', {platform_name} '"
list_devices = list(set(subprocess.getoutput(command).split("\n")))
list_devices = sorted(list_devices, reverse=False)

if platform_name != "web":
    item = list_devices[platform_slot - 1]
    device_name = item[item.find("(") + 1:item.find(")")].split(",")[1].strip()
    device_uid = item[item.find("Found ") + 6:item.find("(")].strip()
    print(f"{device_name}: {device_uid}")

value = (device_uid, browser_name)[platform_name == "web"]  # noqa

with open(str(ENV_FILE).format(f"{option.env}"), "r+") as f:
    content = yaml.safe_load(f)
    if option.main:
        content["sync"][f"main_{platform_name.lower()}"] = value
    else:
        content["sync"]["platforms"][platform_name.lower()] = value
    f.seek(0)
    yaml.dump(content, f)
    f.truncate()
