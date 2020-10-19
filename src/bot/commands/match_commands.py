from src.lib import endpoints
from src import constants
from src.bot.models.user import User
from src.bot.models.sessions import create_session
from src.bot.services import user_services
from src.bot.commands import helpers


def run_last_match_command(update, context):
    chat_id = update.message.chat_id
    telegram_handle = update.message.from_user.username

    user = user_services.lookup_user_by_telegram_handle(telegram_handle)

    if not user:
        update.message.reply_text(constants.USER_NOT_REGISTERED_MESSAGE)

    response, status_code = endpoints.get_player_recent_matches_by_account_id(
        user.account_id
    )

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        update.message.reply_text(constants.BAD_RESPONSE_MESSAGE)

    output_message = helpers.create_last_match_message(response[0])
    update.message.reply_text(output_message)
