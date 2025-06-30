import os
import subprocess
import sys


def get_app_version_and_build(app_name):
    # Construct the full path to the application
    app_path = os.path.join('/Applications', f'{app_name}.app')
    plist_path = os.path.join(app_path, 'Contents', 'Info.plist')

    try:
        # Use defaults to get CFBundleShortVersionString (version) and CFBundleVersion (build)
        version = subprocess.run(
            ['defaults', 'read', plist_path, 'CFBundleShortVersionString'],
            capture_output=True,
            text=True
        ).stdout.strip()

        build = subprocess.run(
            ['defaults', 'read', plist_path, 'CFBundleVersion'],
            capture_output=True,
            text=True
        ).stdout.strip()

        return version, build
    except subprocess.CalledProcessError:
        return "Error retrieving version and build", None
    except Exception as e:
        return str(e), None


app_name = sys.argv[1]
version, build = get_app_version_and_build(app_name)
print(f"{version} - build {build}")

# Usage: python3 src/find_flo_mac_version.py Flo
# Usage: python3 src/find_flo_mac_version.py FloInternal
