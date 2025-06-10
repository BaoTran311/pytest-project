from pathlib import Path

# Project directory
PROJECT_ROOT = Path(__file__).parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"
RECORD_DIR = PROJECT_ROOT / "records"
ENV_DIR = PROJECT_ROOT / "config"

# Element timeout
TIMEOUT = 10
DISPLAY_TIMEOUT = 3

# General config
PYTHON_CONFIG = "pythonConfig"

# General projects
LCL_PREFIX = "[DEL]"  # delete all objects (Local) having the prefix
GBL_PREFIX = "[GBL]"  # Almost general data (Global)

# Datetime Format
FMT_TIME = "%Y%m%dT%H%M%S"
FMT_TIME_Z = "%Y%m%dT%H%M%SZ"

# Retries
RETRIES = 3  # Use in Recursive
POLLING = 5  # Time a sec (time.sleep)
