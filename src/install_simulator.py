# !/usr/bin/python3
import optparse
import os
import re
import subprocess
from pathlib import Path

from src.consts import ENV_DIR
from src.utils import yaml_util

parser = optparse.OptionParser(usage="%prog [-d][-i]", version="%prog 1.0.0")
parser.add_option("-m", "--main", help="Main platform that synchronizes CRUD data with another")
parser.add_option("-p", "--platforms", help="Platforms that verify synchronizes data")
parser.add_option("-e", "--env", help="Environment file")

(option, args) = parser.parse_args()
"""
Example executive command
python3 ci_execute.py -m 'mac, /Users/baotran/Desktop/Flo_v0.9.32_24032001.dmg' -p '
      iPad Pro (12.9-inch) (6th generation), 16.4, /Users/baotran/Desktop/Flo.0.9.19.23102601.app
      iPhone 14 Pro Max, 16.4, /Users/baotran/Desktop/FloiOS_0.9.49_202312271238.app
      web, chrome
      mac, /Users/baotran/Desktop/FloInternal_v0.9.32_24032001.dmg
' -e staging_4913
----------
python3 ci_execute.py -m 'web, chrome' -p '
      iPad Pro (12.9-inch) (6th generation), 16.4, /Users/baotran/Desktop/Flo.0.9.19.23102601.app
      iPhone 14 Pro Max, 16.4, /Users/baotran/Desktop/FloiOS_0.9.49_202312271238.app
      web, chrome
      mac, /Users/baotran/Desktop/FloInternal_v0.9.32_24032001.dmg
' -e staging_4913
----------
python3 ci_execute.py -m 'web, chrome' -p '
      iPad, false
      iPhone, false
      web, chrome
      mac, /Users/baotran/Desktop/FloInternal_v0.9.32_24032001.dmg
' -e staging_4913
"""
len_line = 12
_config = yaml_util.load(ENV_DIR / f"{option.env}.yaml")


def __installappsimulator__(device_name, ios_version, install_path):  # noqa
    command = f"""xcrun simctl list devices | grep -A {len_line} ' iOS {ios_version}' | grep '{device_name}' | grep -m 1 -o '{device_name}.*'"""
    device_info = subprocess.getoutput(command)
    pattern = "[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}"
    device_uid = re.findall(pattern, device_info)[-1]
    os.system(f'open -a Simulator --args -CurrentDeviceUDID "{device_uid}"')
    os.system(f'xcrun simctl boot "{device_uid}"')
    bundle_id = 'com.floware.universalflo.staging' if "iPad" in device_name else 'com.floware.flo.staging'
    os.system(f'xcrun simctl uninstall "{device_uid}" {bundle_id}')
    os.system(f'xcrun simctl install "{device_uid}" {install_path}')
    return device_uid


def __installmac__(install_path):  # noqa
    is_internal = "internal" in install_path.lower()
    sub_name = "Internal" if is_internal else ""
    # Remove the Quarantine Extended Attribute of the file to avoid the alert popup:
    # "Flo" can't be opened because Apple cannot check it for malicious software.
    subprocess.getoutput(f"xattr -d com.apple.quarantine {install_path}")
    app_data_dir = Path.home() / f"Library/Containers/com.floware.flomac{'.internal' if is_internal else ''}"
    os.system(f"rm -rf {app_data_dir}")  # delete existing Flo app data
    os.system(f"rm -rf {app_data_dir}.FloShare")  # delete existing FloShare app data
    os.system(f"rm -rf /Applications/Flo{sub_name}.app")  # delete existing FloShare app data
    # Install the app
    os.system(f"hdiutil attach {install_path} > /dev/null")  # '> /dev/null' hide this command's console output
    os.system(f"ditto --rsrc /Volumes/Flo{sub_name}/Flo{sub_name}.app /Applications/Flo{sub_name}.app")
    os.system(f"hdiutil detach /Volumes/Flo{sub_name} > /dev/null")
    return f"com.floware.flomac{'.internal' if is_internal else ''}"


main_sync_info = tuple(option.main.split(", "))
main_sync_platform = main_sync_info[0].split(" ")[0].lower()

_config['sync'][f"main_{main_sync_platform}"] = __installappsimulator__(*main_sync_info) \
    if main_sync_platform in ("iphone", "ipad") else (
    __installmac__(main_sync_info[1].strip()) if 'mac' in main_sync_platform else main_sync_info[1]
)

# turn off the main device without testing
for k, v in _config['sync'].items():
    if main_sync_platform not in k and k.startswith("main"):
        _config['sync'][k] = "false"

for platform in option.platforms.strip().split("\n"):
    _info = tuple(platform.strip().split(", "))
    platform_name = _info[0].split(" ")[0].lower()
    if "false" in _info[1].strip():
        _config['sync']['platforms'][platform_name] = "false"
        continue
    match platform_name:
        case "iphone" | "ipad":
            _config['sync']['platforms'][platform_name] = __installappsimulator__(*_info)
        case "mac":
            _config['sync']['platforms'][platform_name] = __installmac__(_info[1].strip())
        case _:
            _info[1].strip()

yaml_util.dump(str(ENV_FILE).format(f"{option.env}"), _config)