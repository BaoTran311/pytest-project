import logging
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from src.apps.consts import LOG_DIR
from src.utils import logger, file_util

logging.getLogger('WDM').setLevel(logging.NOTSET)

if eval(os.getenv("RUN_REMOTE", "False")):
    DEFAULT_HOST = os.getenv("REMOTE_IP")


def create_chrome_driver(client, *, headless=False, user_profile: str = None) -> WebDriver:
    run_remote = eval(os.getenv("RUN_REMOTE", "False"))
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("-headless")
    if user_profile:
        file_util.create_folder(user_profile)
        options.add_argument(f"--user-data-dir={user_profile}")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        # 'download.default_directory': DOWNLOAD_DIR,
        'download.directory_upgrade': True,
        'download.prompt_for_download': False
    })
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    try:
        service = ChromeService(ChromeDriverManager().install(), log_output=str(LOG_DIR / f"chrome_{client}.log"))
        driver = webdriver.Remote(command_executor=f"http://{DEFAULT_HOST}:4444/wd/hub", options=options) if \
            run_remote else webdriver.Chrome(service=service, options=options)

        driver.implicitly_wait(3)
        driver.maximize_window()
        if headless:
            # Unable to full screen in headless mode https://bugs.chromium.org/p/chromium/issues/detail?id=737535
            driver.set_window_size(1920, 1080)
        return driver
    except Exception as ex:
        logger.error(ex)
        raise f"Failed to create Chrome browser driver: {ex}" from ex


def create_firefox_driver(client, *, headless=False, user_profile: str = None):
    run_remote = eval(os.getenv("RUN_REMOTE", "False"))
    options = Options()
    if headless:
        options.add_argument("-headless")
    options.add_argument("-private")
    if user_profile:
        options.add_argument(f"--user-data-dir={user_profile}")
    try:
        service = FirefoxService(GeckoDriverManager().install(), log_output=str(LOG_DIR) + f"gecko_{client}.log")
        # driver = webdriver.Firefox(service=service, options=options)
        driver = webdriver.Remote(command_executor=f"http://{DEFAULT_HOST}:5555/wd/hub", options=options) if \
            run_remote else webdriver.Firefox(service=service, options=options)
        driver.implicitly_wait(3)
        driver.maximize_window()
        if headless:
            driver.set_window_size(1920, 1080)
        return driver
    except Exception as ex:
        logger.error(ex)
        raise Exception("Failed to create Firefox browser driver: %s" % ex)
