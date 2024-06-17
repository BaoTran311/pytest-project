import pytest

from src.data_runtime import DataRuntime
from src.utils import logger
from src.utils.assert_util import verify


@pytest.mark.parametrize("invalid_field", ("username", "password"))
def test(flo_web, invalid_field):
    logger.info("Step 1: Navigate to flo web")
    flo_web.navigate_to_flo_web()

    logger.info("Step 2: Login with invalid account")
    credential = [DataRuntime.config.user, DataRuntime.config.password]
    credential[1 if invalid_field == "username" else 0] = "asdf"
    flo_web.login_page.login(*credential)

    expected_msg = "Incorrect password/username. Please try again."
    verify(
        flo_web.login_page.is_error_text_is_displayed_with_correct_content(expected_msg),
        f"Verify error text '{expected_msg!r}' displays"
    )
