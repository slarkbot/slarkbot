from src.lib import endpoints
from src import constants
from src.bot.models.user import User
from src.bot.models.sessions import create_session
from src.bot.services import user_services
from src.bot.commands import helpers
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def run_last_match_command(update, context):
    chat_id = update.message.chat_id
    try:
        telegram_handle = context.args[0]
    except (IndexError, ValueError):
        telegram_handle = update.message.from_user.username

    user = user_services.lookup_user_by_telegram_handle(telegram_handle)

    if not user:
        update.message.reply_text(constants.USER_NOT_REGISTERED_MESSAGE)

    response, status_code = endpoints.get_player_recent_matches_by_account_id(
        user.account_id
    )

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        update.message.reply_text(constants.BAD_RESPONSE_MESSAGE)

    output_message = helpers.create_match_message(response[0])
    button = InlineKeyboardButton("Full match details", callback_data=("match " + str(response[0]["match_id"])))
    markup = InlineKeyboardMarkup.from_button(button)
    update.message.reply_text(output_message, reply_markup=markup)


def run_get_match_by_match_id(update, context):
    chat_id = update.message.chat_id
    telegram_handle = update.message.from_user.username

    try:
        match_id = context.args[0]
        match_id = int(match_id)
    except (IndexError, ValueError):
        update.message.reply_text(
            "That isn't a match ID\. Use `/match <match id here>`",
            parse_mode="MarkdownV2"
        )
        return

    response, status_code = endpoints.get_match_by_id(match_id)

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        update.message.reply_text(constants.BAD_RESPONSE_MESSAGE)

    output_message = helpers.create_match_detail_message(response)
    update.message.reply_text(output_message)

def handle_match_details_callback(update, context):
    query = update.callback_query

    match_id = int(query.data.replace("match ", ""))

    response, status_code = endpoints.get_match_by_id(match_id)

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        query.answer(constants.BAD_RESPONSE_MESSAGE)
        return

    output_message = helpers.create_match_detail_message(response)

    query.answer()
    query.message.edit_text(output_message)
