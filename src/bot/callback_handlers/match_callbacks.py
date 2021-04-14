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

    button1 = InlineKeyboardButton(
        "Scoreboard",
        callback_data=("match " + str(response["match_id"]))
    )

    button2 = InlineKeyboardButton(
        "Players/Ranks",
        callback_data=("match " + str(response["match_id"]) + " players")
    )

    button3 = InlineKeyboardButton(
        "Damage/Heal",
        callback_data=("match " + str(response["match_id"]) + " damage")
    )

    button4 = InlineKeyboardButton(
        "Order",
        callback_data=("match " + str(response["match_id"]) + " order")
    )

    buttons = [button1, button2, button3, button4]

    markup = InlineKeyboardMarkup.from_column(buttons)
    
    query.message.edit_text(
        output_message, parse_mode="MarkdownV2", reply_markup=markup, disable_web_page_preview=True
    )
