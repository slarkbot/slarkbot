from src.bot.models.user import User
from src.bot.models.sessions import create_session
from src.bot.services import user_services
from src.bot.commands import helpers
from src.lib import endpoints
from src import constants


def save_user(user):
    session = create_session()
    session.add(user)
    session.commit()


def run_register_command(update, context):
    chat_id = update.message.chat_id
    telegram_handle = update.message.from_user.username

    if user_services.lookup_user_by_telegram_handle(telegram_handle):
        return update.message.reply_text(
            f"I already have a handle for @{telegram_handle}, sorry :("
        )

    try:
        account_id = context.args[0]
        new_user = User(telegram_handle, account_id, chat_id)
        save_user(new_user)
        update.message.reply_text(f"Successfully registered user {telegram_handle}")
    except (IndexError, ValueError):
        update.message.reply_text("No dota friend ID was given")


def run_get_player_recents_command(update, context):
    chat_id = update.message.chat_id
    telegram_handle = update.message.from_user.username

    registered_user = user_services.lookup_user_by_telegram_handle(telegram_handle)

    if not registered_user:
        update.message.reply_text(
            "Could not find an account ID. Register your telegram handle using `/register`"
        )

    account_id = registered_user.account_id

    limit = constants.QUERY_PARAMETERS.RESPONSE_LIMIT.value
    if context.args:
        try:
            limit = context.args[0]
            limit = int(limit)
        except ValueError:
            update.message.reply_text(
                "Oops, you gave me an invalid argument. Use `/recents <number>` or `/recents`"
            )

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

    output_message = f"{persona_name} is {rank}"
    update.message.reply_text(output_message)
