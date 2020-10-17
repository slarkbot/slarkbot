#!/usr/bin/env python

from dotenv import load_dotenv
from src.lib.endpoints import get_health_check
from src.config import check_config
from src.bot import bot_factory


def main():
    load_dotenv()
    check_config()

    updater = bot_factory.create_bot()

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
