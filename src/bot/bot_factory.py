import os
from telegram.ext import Updater, CommandHandler

from src.bot import logger_factory
from src.bot.commands import health_check_command
from src.bot.commands import user_commands
from src.constants import LOG_LEVEL_MAP


def create_bot():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    logger = logger_factory.create_logger()
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("status", health_check_command.run_health_check))
    dp.add_handler(CommandHandler("register", user_commands.run_register_command))
    dp.add_handler(
        CommandHandler("recents", user_commands.run_get_player_recents_command)
    )

    return updater, logger
