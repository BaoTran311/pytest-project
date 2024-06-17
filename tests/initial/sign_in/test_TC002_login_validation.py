from src.data_runtime import DataRuntime
from src.utils import logger
from src.utils.assert_util import verify


def test(flo_web, flo_iphone):
    logger.info("Step 1: Navigate to flo web")
    flo_web.navigate_to_flo_web()

    logger.info("Step 2: Login with valid account")
    flo_web.login_page.login(DataRuntime.config.user, DataRuntime.config.password)
    flo_web.home_page.wait_for_homepage_displayed()

    verify(flo_web.home_page.is_homepage_displays(), "Verify user login successfully")
