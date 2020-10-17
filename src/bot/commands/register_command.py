from src.bot.models.user import User
from src.bot.models import database_engine
from src.bot.models.sessions import create_session


def save_user(user):
    session = create_session(database_engine)
    session.add(user)
    session.commit()


def run_register_command(update, context):
    chat_id = update.message.chat_id
    telegram_handle = update.message.from_user.username

    try:
        account_id = context.args[0]
        new_user = User(telegram_handle, account_id, chat_id)
        save_user(new_user)
        update.message.reply_text(f"Successfully registered user {telegram_handle}")
    except (IndexError, ValueError):
        update.message.reply_text("No account ID was given")
