from src.bot.models.user import User
from src.bot.models.sessions import create_session


def lookup_user_by_telegram_handle(telegram_handle):
    telegram_handle = telegram_handle.lower().replace("@", "")
    session = create_session()
    return session.query(User).filter(User.telegram_handle == telegram_handle).first()


def lookup_user_by_account_id(account_id):
    account_id = int(account_id)
    session = create_session()
    return session.query(User).filter(User.account_id == account_id).first()
