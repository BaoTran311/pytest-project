import logging
import platform

from src import consts

logger = logging.getLogger(consts.PYTHON_CONFIG)
logging.getLogger("urllib3").setLevel(logging.ERROR)  # disable urllib3 Retrying warning messages


def create_handler_logger(log_level):
    os_name = platform.system()
    logging.basicConfig(level=logging.INFO)

    for _handler in logger.handlers[:]:
        logger.removeHandler(_handler)

    logger.propagate = False
    stream = logging.StreamHandler()
    stream.setLevel(log_level)

    if os_name == "Windows":
        LOG_FORMAT_WIN = "\t%(asctime)-6s %(levelname)7s | %(message)s"
        formatter = logging.Formatter(LOG_FORMAT_WIN, "%H:%M:%S")
    else:
        from colorlog import ColoredFormatter
        LOG_FORMAT = "\t%(asctime)-6s %(log_color)s%(levelname)7s | %(log_color)s%(message)s"
        formatter = ColoredFormatter(LOG_FORMAT, "%H:%M:%S")

    stream.setFormatter(formatter)
    logger.setLevel(log_level)
    logger.addHandler(stream)


class dotdict(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

    def __getitem__(self, key):
        res = super().__getitem__(key)
        if isinstance(res, dict):
            self[key] = dotdict(res)
        elif isinstance(res, list):
            for i in range(len(res)):
                if isinstance(res[i], dict):
                    res[i] = dotdict(res[i])
        return super().__getitem__(key)  # reload value again to get dotdict effect

    def __missing__(self, key):
        return rf"[~~missing-key-{key}~~]"
