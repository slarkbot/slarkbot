from src.bot.models.user import User
from src.bot.models.sessions import create_session
from src.bot.services import user_services
from src.bot.commands import helpers
from src.lib import endpoints
from src import constants


def save_user(user):
    user.telegram_handle = user.telegram_handle.lower()
    session = create_session()
    session.merge(user)
    session.commit()


def run_register_command(update, context):
    chat_id = update.message.chat_id
    telegram_handle = update.message.from_user.username

    try:
        account_id = context.args[0]

        user = user_services.lookup_user_by_telegram_handle(telegram_handle) or User(
            telegram_handle, account_id, chat_id
        )
        user.account_id = account_id
        save_user(user)
        update.message.reply_text(
            f"Successfully registered user {telegram_handle} as {account_id}"
        )
    except (IndexError, ValueError):
        update.message.reply_text("No dota friend ID was given")


def run_get_player_recents_command(update, context):
    chat_id = update.message.chat_id

    # Assume defaults
    registered_user = user_services.lookup_user_by_telegram_handle(
        update.message.from_user.username
    )
    limit = constants.QUERY_PARAMETERS.RESPONSE_LIMIT.value

    for arg in context.args:
        user = user_services.lookup_user_by_telegram_handle(arg)
        if user:
            registered_user = user
        try:
            limit = int(arg)
        except:
            pass

    if not registered_user:
        update.message.reply_text(
            "Could not find that username. If you're looking for your own matches, register your telegram handle using `/register`"
        )

    account_id = registered_user.account_id

    if limit > 20:
        limit = 20

    response, status_code = endpoints.get_player_recent_matches_by_account_id(
        account_id
    )

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        update.message.reply_text(constants.BAD_RESPONSE_MESSAGE)

    output_message = helpers.create_recent_matches_message(response[:limit])
    update.message.reply_text(output_message)


def run_get_player_rank_command(update, context):
    chat_id = update.message.chat_id
    try:
        telegram_handle = context.args[0]
    except(IndexError, ValueError):
        telegram_handle = update.message.from_user.username
    telegram_handle = telegram_handle.replace("@", "")

    registered_user = user_services.lookup_user_by_telegram_handle(telegram_handle)

    if not registered_user:
        update.message.reply_text(
            "Could not find an account ID. Register your telegram handle using `/register`"
        )

    account_id = registered_user.account_id

    response, status_code = endpoints.get_player_rank_by_account_id(account_id)

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        update.message.reply_text("An unknown error occured, sorry D:")

    persona_name = response["profile"]["personaname"]
    rank_tier = response["rank_tier"]

    rank = helpers.map_rank_tier_to_string(rank_tier)

    output_message = f"{persona_name} (@{telegram_handle}) is {rank}"
    update.message.reply_text(output_message)
