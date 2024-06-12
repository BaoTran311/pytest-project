import pytest

from src.data_runtime import DataRuntime
from src.utils import logger


@pytest.mark.parametrize("invalid_field", ("username", "password"))
def test_login_with_invalid_account(page, invalid_field):
    logger.info("Step 1: Navigate to flo web")
    page.navigate_to_flo_web()

    logger.info("Step 2: Login with valid account")
    credential = [DataRuntime.config.user, DataRuntime.config.password]
    credential[1 if invalid_field == "username" else 0] = "asdf"
    page.login_page.login(*credential)

    logger.info("Verify error text is displayed with correct content")
    page.login_page.verify_error_text_is_displayed_with_correct_content("Incorrect password/username. Please try again.")
