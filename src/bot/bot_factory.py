import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from src.bot import logger_factory
from src.bot.commands import health_check_command
from src.bot.commands import user_commands
from src.bot.commands import help_command
from src.bot.commands import match_commands

from src.bot.message_handlers.freedom_units import convert_to_freedom_units

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
    dp.add_handler(CommandHandler("help", help_command.run_help_command))
    dp.add_handler(CommandHandler("lastmatch", match_commands.run_last_match_command))
    dp.add_handler(CommandHandler("match", match_commands.run_get_match_by_match_id))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, convert_to_freedom_units))

    return updater, logger
