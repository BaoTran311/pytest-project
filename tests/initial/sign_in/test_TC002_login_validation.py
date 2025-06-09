import pytest

from src.data_runtime import DataRuntime
from src.utils import logger
from src.utils.assert_util import verify


def test(web):
    logger.info("Step 1: Navigate to flo web")
    web.navigate_to_flo_web()

    logger.info("Step 2: Login with invalid account")
    web.login_page.login("asdf", "asdf")
    expected_msg = "Incorrect password/username. Please try again"
    verify(
        web.login_page.is_error_text_is_displayed_with_correct_content(expected_msg),
        f"Verify error text '{expected_msg!r}' displays"
    )

    # logger.info("Step 3: Login with valid account")
    # web.login_page.refresh()
    # web.login_page.login(DataRuntime.config.user, DataRuntime.config.password)
    # web.top_navigation.wait_for_top_navigation_displayed()
    # verify(web.top_navigation.wait_for_top_navigation_displayed() is False, "Verify user login successfully")


@pytest.fixture(autouse=True)
def bao(web):
    web.login_page.login("asdf", "asdf")
    yield
    web.login_page.login("asdf", "asdf")
