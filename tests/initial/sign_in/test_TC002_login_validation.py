from src.data_runtime import DataRuntime
from src.utils import logger


def test_login_validation(page):
    logger.info("Step 1: Navigate to flo web")
    page.navigate_to_flo_web()

    logger.info("Step 2: Login with valid account")
    page.login_page.login(DataRuntime.config.user, DataRuntime.config.password)

    logger.info("Verify user login successfully")
    page.home_page.verify_homepage_displays()
