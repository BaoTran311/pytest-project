import time

import allure

from src.data_runtime import DataRuntime
from src.utils import logger
from src.utils.assert_util import verify


# @allure.testcase("TC1 - Login with valid credential")
def test(web):
    logger.info("Step 1: Navigate to flo web")
    web.navigate_to_aquariux()

    logger.info("Step 2: Login with valid account")
    web.login_page.login_with_demo_account(DataRuntime.config.user, DataRuntime.config.password)
    time.sleep(5)
    verify(
        True,
        f"Verify homepage displays after login success"
    )

    logger.info("Step 3: Test failed")
    verify(
        False,
        f"Verify failed"
    )
