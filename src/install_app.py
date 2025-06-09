# !/usr/bin/python3
import optparse
import os
import re
import subprocess

import yaml

from apps.consts import ENV_FILE

parser = optparse.OptionParser(usage="%prog [-d][-i]", version="%prog 1.0.0")
parser.add_option("-m", "--main", action="store_true", default=False)
parser.add_option("-p", "--platforms", help="Platforms that verify synchronizes data")
parser.add_option("-e", "--env", help="Environment file")

(option, args) = parser.parse_args()
"""
Below are example executive commands
----------
python3 src/install_app.py --main -p 'iPad Pro (12.9-inch) (6th generation), 16.4, /Users/<user>/Desktop/Flo.0.9.19.23102601.app' -e staging_4913
python3 src/install_app.py -p 'iPad Pro (12.9-inch) (6th generation), 16.4, /Users/<user>/Desktop/Flo.0.9.19.23102601.app' -e staging_4913
python3 src/install_app.py -p 'mac, /Users/<user>/Desktop/FloInternal_v0.9.32_24032001.dmg' -e staging_4913 --main
python3 src/install_app.py -p 'iPhone 14 Pro Max, 16.4, /Users/<user>/Desktop/FloiOS_0.9.49_202312271238.app' -e staging_4913 -m
----------
"""


def __installmac__(install_path):  # noqa
    # Sort to make sure index will be flo internal > flo
    flo_internal, flo = sorted(list(filter(lambda file: file.endswith(".dmg"), os.listdir(install_path))))
    is_internal = not option.main
    install_path += ("/", "")[install_path.endswith("/")] + (flo, flo_internal)[is_internal]
    sub_name = "Internal" if is_internal else ""
    # Remove the Quarantine Extended Attribute of the file to avoid the alert popup:
    # "Flo" can't be opened because Apple cannot check it for malicious software.
    subprocess.getoutput(f"xattr -d com.apple.quarantine {install_path}")
    """
    - Use below code incase user want to re-install instead of overriding
    app_data_dir = Path.home() / f"Library/Containers/com.floware.flomac{'.internal' if is_internal else ''}"
    os.system(f"rm -rf {app_data_dir}")  # delete existing Flo app data
    os.system(f"rm -rf {app_data_dir}.FloShare")  # delete existing FloShare app data
    os.system(f"rm -rf /Applications/Flo{sub_name}.app")  # delete existing FloShare app data
    """
    # Install the app
    os.system(f"hdiutil attach {install_path} > /dev/null")  # '> /dev/null' hide this command's console output
    os.system(f"ditto --rsrc /Volumes/Flo{sub_name}/Flo{sub_name}.app /Applications/Flo{sub_name}.app")
    os.system(f"hdiutil detach /Volumes/Flo{sub_name} > /dev/null")
    return f"com.floware.flomac{'.internal' if is_internal else ''}"


def __installappsimulator__(device_name, ios_version, install_path):  # noqa
    command = f"""xcrun simctl list devices | grep -A 12 ' iOS {ios_version}' | grep '{device_name}' | grep -m 1 -o '{device_name}.*'"""
    device_info = subprocess.getoutput(command)
    pattern = "[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}"
    device_uid = re.findall(pattern, device_info)[-1]
    os.system(f'open -a Simulator --args -CurrentDeviceUDID "{device_uid}"')
    # Execute the command and do not print the error 'Unable to boot device in current state: Booted' on the console
    output = subprocess.getoutput(f'xcrun simctl boot " {device_uid}"')
    bundle_id = 'com.floware.universalflo.staging' if "iPad" in device_name else 'com.floware.flo.staging'
    os.system(f'xcrun simctl uninstall "{device_uid}" {bundle_id}')
    os.system(f'xcrun simctl install "{device_uid}" {install_path}')
    return device_uid


_info = option.platforms.strip().split(", ")
platform_name = _info[0].split(" ")[0].lower()
match platform_name:
    case "iphone" | "ipad":
        value = __installappsimulator__(*_info)
    case "mac":
        value = __installmac__(_info[1].strip())
    case _:
        value = ""

with open(str(ENV_FILE).format(f"{option.env}"), 'r+') as f:
    content = yaml.load(f, Loader=yaml.SafeLoader)
    if option.main:
        content['sync'][f'main_{platform_name}'] = value
    else:
        content['sync']['platforms'][platform_name] = value
    f.seek(0)
    yaml.dump(content, f, sort_keys=False)
    f.truncate()
