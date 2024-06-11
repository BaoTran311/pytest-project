import fileinput
import logging
import platform

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from src import consts

_logger = logging.getLogger(consts.PYTHON_CONFIG)


def create_chrome_driver(
        *,
        headless=False,
        full_screen=False,
        extension=None,
        user_profile: str = None,
) -> WebDriver:
    try:
        os_name = platform.system()  # Mac: Darwin | Win: Windows | Linux: Linux
        chrome_options = webdriver.ChromeOptions()

        # Added argument general
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("-disable-setuid-sandbox")

        if headless:
            chrome_options.add_argument("--headless")
        elif full_screen:
            chrome_options.add_argument("--start-fullscreen")
        else:
            chrome_options.add_argument("--start-maximized")

        if user_profile:
            user_path = ""
            if os_name == "Windows":
                user_path = f"{user_profile}\\Default\\Preferences"

            with fileinput.FileInput(user_path, inplace=True, backup='.bak') as _f:
                for line in _f:
                    print(line.replace('Crashed', 'none'), end='')

        if extension:
            chrome_options.add_argument(f"--load-extension={extension}")

        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option(
            "prefs", {
                "credentials_enable_service": False,
                "download.directory_upgrade": True,
                "download.prompt_for_download": False,
                "profile": {"password_manager_enabled": False}
            }
        )

        # init driver
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        if headless:
            # Unable to full screen in headless mode
            # Issue: https://bugs.chromium.org/p/chromium/issues/detail?id=737535
            driver.set_window_size(1920, 1080)
        else:
            # driver.maximize_window()
            driver.set_window_size(1380, 1080)

        return driver
    except Exception as ex:
        _logger.critical(" > Failed to create Chrome browser driver")
        print()  # Empty line in CLI
        raise ex
