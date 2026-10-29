import logging

from colorlog import ColoredFormatter

LOG_FORMAT = (
    "%(log_color)s%(levelname)s:%(reset)s "
    "%(name_log_color)s[%(asctime)s]%(reset)s "
    "%(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger():
    formatter = ColoredFormatter(
        LOG_FORMAT,
        datefmt=DATE_FORMAT,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={
            "name": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red",
            },
        },
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        logger.propagate = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
