import os

import pytest
from appium import webdriver
from appium.options.ios import XCUITestOptions, SafariOptions
from appium.options.mac import Mac2Options
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.webdriver import WebDriver

from src.apps.consts import PROJECT_ROOT
from src.utils import logger

DEFAULT_HOST = "127.0.0.1"
if eval(os.getenv("RUN_REMOTE", "False")):
    DEFAULT_HOST = os.getenv("REMOTE_IP")


def start_appium_server(server_port=4723, webdriver_agent_port=8100):
    os.system(f"lsof -ti tcp:{server_port} | xargs kill")  # kill the listening port
    appium_service = AppiumService()
    args = [
        "-pa", "/",
        "--port", str(server_port),
        "--driver-xcuitest-webdriveragent-port", str(webdriver_agent_port),
        "--log", str(PROJECT_ROOT) + f"/_logs/appium_{server_port}.log"
    ]
    appium_service.start(args=args, timeout_ms=10000)
    if not appium_service.is_running:
        error = f"Failed to start Appium server 'http://{DEFAULT_HOST}:{server_port}'"
        logger.error()
        raise Exception(error)
    return appium_service


def create_ios_driver(device_udid: str, bundle_id: str, appium_server_port=4723, wda_port=8100) -> WebDriver:
    # https://appium.github.io/appium-xcuitest-driver/4.24/capabilities/
    options = XCUITestOptions()

    # safari = SafariOptions()
    # safari.device_type = "iPad"
    # safari.device_udid = device_udid
    # safari.use_simulator = False

    # Required options
    options.udid = device_udid
    options.bundle_id = bundle_id
    options.wda_local_port = wda_port
    options.no_reset = True
    options.use_new_wda = eval(os.getenv("NEW_WDA"))

    # Additional options
    options.clear_system_files = True
    options.command_timeouts = 20000
    options.new_command_timeout = 0  # Setting it to zero disables the timer.

    # Simulator only (https://github.com/wix/AppleSimulatorUtils)
    permissions = {
        bundle_id: {
            "notifications": "NO",
            "siri": "NO",
            "photos": "YES",
            "camera": "YES",
            "location": "always"
        }
    }
    # options.permissions = json_util.format(permissions)

    try:
        DEFAULT_HOST = "127.0.0.1"
        return webdriver.Remote(f"{DEFAULT_HOST}:{appium_server_port}", options=options)
        # pytest.set_trace()
        # bao = webdriver.Remote(f"{DEFAULT_HOST}:{appium_server_port}", options=tmp)
        # return bao
    except Exception as ex:
        error = f"Failed to init resources driver with error: {ex}"
        logger.error(error)
        raise Exception(error)


def create_mac_driver(bundle_id: str, appium_server_port=4723, system_port=10100):
    os.system(f"lsof -ti tcp:{system_port} | xargs kill")  # kill the listening port
    options = Mac2Options()

    # Required options
    options.bundle_id = bundle_id
    options.system_port = system_port

    # Additional options
    options.clear_system_files = True
    options.command_timeouts = 20000
    options.new_command_timeout = 0  # setting it to zero disables the timer.
    options.show_server_logs = True  # enable Mac2Driver host process logging.

    try:
        return webdriver.Remote(f"{DEFAULT_HOST}:{appium_server_port}", options=options)
    except Exception as ex:
        error = f"Failed to init resources driver with error: {ex}"
        logger.error(error)
        raise Exception(error)
