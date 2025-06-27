import pytest

from src.data_runtime import DataRuntime
from src.utils import logger
from src.utils.assert_util import verify


@pytest.mark.parametrize("invalid_field", ["username", "password"])
def test(web, invalid_field):
    logger.info("Step 1: Navigate to AQX Trader")
    web.navigate_to_aquariux()

    logger.info(f"Step 2: Login with invalid {invalid_field}")
    credential = [DataRuntime.config.user, DataRuntime.config.password]
    credential[0 if invalid_field == "username" else 1] = f"invalid {invalid_field}"
    web.login_page.login_with_demo_account(*credential)

    expected_msg = "Invalid credentials, please try again"
    verify(
        web.login_page.is_alert_error_displayed_with_correct_content(expected_msg),
        f"Verify error text {expected_msg!r} displays"
    )
