import logging
import os
import sys

from datetime import date

from src.constants import LOG_LEVEL_MAP, DEFAULT_LOG_LEVEL


def create_log_file():
    date_string = date.today().strftime("%d-%m-%y")
    return "./logs/%s.log" % date_string


def create_log_output_directory():
    print("creating logging directory")
    if not os.path.exists("logs"):
        os.makedirs("logs")


def create_logger():
    """
    Creates and returns a logger with log level `log_level` and name
    """

    create_log_output_directory()

    configured_log_level = os.getenv("LOG_LEVEL") or DEFAULT_LOG_LEVEL
    log_level = LOG_LEVEL_MAP[configured_log_level]

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=log_level,
        handlers=[
            logging.FileHandler(create_log_file(), mode="a"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    logger = logging.getLogger(__name__)
    return logger
