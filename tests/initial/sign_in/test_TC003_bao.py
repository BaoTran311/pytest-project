from src.utils import logger


def test(page, iphone):
    logger.info("Step 1: Launch flo iPhone")
    iphone.launch_flo_iphone()

    logger.info("Step 2: Navigate to flo web")
    page.navigate_to_flo_web()

    logger.info("Verify failed")
    assert False
