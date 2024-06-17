import builtins

from pytest_check import check

from src.data_runtime import DataRuntime
from src.utils import logger


def verify(result, msg):
    logger.info(msg)
    if not result:
        builtins.fail_check_point[DataRuntime.tc_info.name].append(msg)  # noqa
    with check:
        assert result
