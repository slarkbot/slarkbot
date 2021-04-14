from functools import wraps
from src.bot.services import user_services


def require_register(func):
    @wraps(func)
    def inner(update, context):
        try:
            telegram_handle = context.args[0]
        except (IndexError, ValueError):
            telegram_handle = update.message.from_user.username

        user = user_services.lookup_user_by_telegram_handle(telegram_handle)

        if not user:
            update.message.reply_markdown_v2(constants.USER_NOT_REGISTERED_MESSAGE)

        func(update, user)

    return inner
