from src.lib import endpoints
from src import constants
from src.bot.commands import helpers
from src.bot.commands import match_helpers
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def handle_match_details_callback(update, context):
    query = update.callback_query

    query_args = query.data.split()
    query_args.pop(0)
    # Args list should now contain only two things, match id and format

    match_id = int(query_args[0])
    try:
        response_format = query_args[1]
    except:
        # Default format if no format is specified
        response_format = "default"

    response, status_code = endpoints.get_match_by_id(match_id)

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        query.answer(constants.BAD_RESPONSE_MESSAGE)
        return

    output_message = match_helpers.create_match_detail_message(
        response, response_format
    )

    query.answer()

    markup = create_inline_keyboard(match_id, response_format)

    query.message.edit_text(
        output_message,
        parse_mode="MarkdownV2",
        reply_markup=markup,
        disable_web_page_preview=True,
    )


def create_inline_keyboard(match_id, response_format="default"):
    match_id = str(match_id)

    button_default = InlineKeyboardButton(
        "Scoreboard", callback_data=(f"match {match_id}")
    )

    button_players = InlineKeyboardButton(
        "Players/Ranks", callback_data=(f"match {match_id} players")
    )

    button_damage = InlineKeyboardButton(
        "Damage/Heal", callback_data=(f"match {match_id} damage")
    )

    button_order = InlineKeyboardButton(
        "Picks/Bans", callback_data=(f"match {match_id} order")
    )

    # Exclude the current view from the inline keyboard
    if response_format == "players":
        buttons = [button_default, button_damage, button_order]
    elif response_format == "damage":
        buttons = [button_default, button_players, button_order]
    elif response_format == "order":
        buttons = [button_default, button_players, button_damage]
    else:
        buttons = [button_players, button_damage, button_order]

    markup = InlineKeyboardMarkup.from_row(buttons)
    return markup
