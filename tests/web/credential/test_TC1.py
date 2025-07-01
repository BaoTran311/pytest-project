from src.utils import logger
from src.utils.assert_util import verify


def test_login_with_valid_credential(web):
    logger.info("Step 1: Navigate to flo web")
    web.navigate_to_aquariux()

    logger.info("Step 2: Login with valid account")
    web.login_page.login_with_demo_account(wait_completed=True)
    verify(
        web.trade_page.top_navigation.is_setting_button_displayed(),
        f"Verify setting button on Top Navigation displays"
    )
    verify(
        web.trade_page.top_navigation.is_switch_theme_button_displayed(),
        f"Verify switch theme button on Top Navigation displays"
    )
    verify(
        web.trade_page.top_navigation.is_notification_button_displayed(),
        f"Verify notification button on Top Navigation displays"
    )
