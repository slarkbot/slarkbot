from src.lib import endpoints
from src import constants
from src.bot.models.user import User
from src.bot.models.sessions import create_session
from src.bot.services import user_services
from src.bot.commands import helpers, match_helpers
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from src.bot.callback_handlers.match_callbacks import create_inline_keyboard
from src.bot.decorators.require_registered_user_decorator import require_register


def run_last_match_command(update, context):
    registered_user = user_services.lookup_user_by_telegram_handle(
        update.message.from_user.username
    )

    args = context.args
    for arg in context.args:
        user = user_services.lookup_user_by_telegram_handle(arg)
        if user:
            registered_user = user
            args.remove(arg)

    if args:
        hero_name = " ".join(args)
        hero_id = helpers.get_hero_id_by_name_or_alias(hero_name)
        if not hero_id:
            update.message.reply_markdown_v2(constants.USER_OR_HERO_NOT_FOUND_MESSAGE)

    if not registered_user:
        update.message.reply_markdown_v2(constants.USER_NOT_REGISTERED_MESSAGE)

    if 'hero_id' in locals():
        response, status_code = endpoints.get_player_matches_by_hero_id(
            registered_user.account_id, hero_id
        )
    else:
        response, status_code = endpoints.get_player_recent_matches_by_account_id(
            registered_user.account_id
        )

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        update.message.reply_text(constants.BAD_RESPONSE_MESSAGE)

    try:
        output_message = match_helpers.create_match_message(response[0])
        button = InlineKeyboardButton(
            "Full match details", callback_data=("match " + str(response[0]["match_id"]))
        )
        markup = InlineKeyboardMarkup.from_button(button)
        update.message.reply_markdown_v2(output_message, reply_markup=markup)
    except IndexError:
        update.message.reply_markdown_v2("I could not find a match by those criteria, sorry\!")


def run_get_match_by_match_id(update, context):
    try:
        match_id = context.args[0]
        match_id = int(match_id)
    except (IndexError, ValueError):
        update.message.reply_markdown_v2(
            "That isn't a match ID\. Use `/match <match id here>`"
        )
        return

    response, status_code = endpoints.get_match_by_id(match_id)

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        update.message.reply_text(constants.BAD_RESPONSE_MESSAGE)

    output_message = match_helpers.create_match_detail_message(response)

    markup = create_inline_keyboard(match_id)
    update.message.reply_markdown_v2(
        output_message, reply_markup=markup, disable_web_page_preview=True
    )
