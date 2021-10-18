from src.bot.models.user import User
from src.bot.models.sessions import create_session


def lookup_user_by_telegram_handle(telegram_handle):
    telegram_handle = telegram_handle.lower().replace("@", "")
    session = create_session()
    bot_user = (
        session.query(User).order_by(User.updated_at.desc().nullslast(), User.user_id.desc()).filter(User.telegram_handle == telegram_handle).first()
    )
    session.close()
    return bot_user


def lookup_user_by_account_id(account_id):
    account_id = int(account_id)

    session = create_session()
    bot_user = session.query(User).order_by(User.updated_at.desc().nullslast(), User.user_id.desc()).filter(User.account_id == account_id).first()
    session.close()
    return bot_user
