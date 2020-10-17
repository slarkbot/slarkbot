#!/usr/bin/env python

import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from src.lib.endpoints import get_health_check
from src.config import check_config
from src.bot import bot_factory


def main():
    check_config()

    updater, logger = bot_factory.create_bot()
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
