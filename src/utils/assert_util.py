import builtins

from pytest_check import check

from src.data_runtime import DataRuntime
from src.utils import logger, datetime_util

_passed_icon = "✓"
_failed_icon = "✘"


def verify(result, msg):
    logger.info(f"{_passed_icon if result else _failed_icon} {msg}")
    if not result:
        attachments = dict()
        for platform, driver in getattr(builtins, "dict_driver").items():
            attach_name = f"{platform}_{datetime_util.get_current_time(time_format="%d-%Y-%m_%H:%M:%S")}.png"
            attachments |= {f"{msg}": [attach_name, driver.get_screenshot_as_png()]}
        builtins.fail_check_point[DataRuntime.tc_info.name].append(attachments)  # noqa

    with check:
        assert result
