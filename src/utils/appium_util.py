import builtins
import os

from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.options.mac import Mac2Options
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.webdriver import WebDriver

from src.consts import PROJECT_ROOT
from src.data_runtime import DataRuntime
from src.utils import logger

DEFAULT_HOST = "127.0.0.1"


def start_appium_server(server_port=4723, webdriver_agent_port=8100, platform=None) -> AppiumService:
    os.system(f"lsof -ti tcp:{server_port} | xargs kill")  # kill the listening port
    appium_service = AppiumService()
    args = [
        "-pa", "/wd/hub",
        "--port", str(server_port),
        "--driver-xcuitest-webdriveragent-port", str(webdriver_agent_port),
        "--log", str(PROJECT_ROOT) + f"/_logs/{server_port}_{platform}.log"
    ]
    appium_service.start(args=args, timeout_ms=10000)
    if not appium_service.is_running:
        error = f"Failed to start Appium server 'http://{DEFAULT_HOST}:{server_port}'"
        logger.error()
        raise Exception(error)
    return appium_service


def create_ios_driver(device_uid: str, bundle_id: str, appium_server_port=4723, wda_port=8100) -> WebDriver:
    # https://appium.github.io/appium-xcuitest-driver/4.24/capabilities/
    options = XCUITestOptions()

    # Required options
    options.udid = device_uid
    options.wda_local_port = wda_port

    # Additional options
    if bundle_id is not None:
        options.bundle_id = bundle_id
    options.clear_system_files = True
    options.command_timeouts = 20000
    options.new_command_timeout = 0  # Setting it to zero disables the timer.
    options.no_reset = DataRuntime.runtime_option.no_reset
    if DataRuntime.config.platforms.get("ipad", None):
        options.orientation = "LANDSCAPE"

    try:
        return webdriver.Remote(f"{DEFAULT_HOST}:{appium_server_port}", options=options)
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


def init_appium_server(platform):
    logger.info(f"Starting {platform} appium server ...")
    service = start_appium_server(
        *[v for k, v in DataRuntime.config.platforms[platform.lower()].items() if k in ("appium", "wda", "system")],
        platform
    )
    builtins.appium_services.append(service)
    return service


def init_appium_driver(platform):
    logger.info(f"Starting {platform} appium driver ...")
    match platform.lower():
        case "iphone" | "ipad":
            driver = create_ios_driver(*[arg for arg in DataRuntime.config.platforms[platform.lower()].values()])
        case "mac":
            driver = create_mac_driver(**DataRuntime.config.platforms.mac)

    builtins.dict_driver[platform] = driver
    return driver
