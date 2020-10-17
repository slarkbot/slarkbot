import logging
import os

from src.constants import LOG_LEVEL_MAP, DEFAULT_LOG_LEVEL


def create_logger():
    """
    Creates and returns a logger with log level `log_level` and name 
    """

    configured_log_level = os.getenv('LOG_LEVEL') or DEFAULT_LOG_LEVEL
    log_level = LOG_LEVEL_MAP[configured_log_level]

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=log_level
    )

    logger = logging.getLogger(__name__)
    return logger
