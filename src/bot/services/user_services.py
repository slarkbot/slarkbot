from src.bot.models.user import User
from src.bot.models.sessions import create_session


def lookup_user_by_telegram_handle(telegram_handle):
    telegram_handle = telegram_handle.lower().replace("@", "")
    session = create_session()
    bot_user = (
        session.query(User).filter(User.telegram_handle == telegram_handle).first()
    )
    return bot_user
