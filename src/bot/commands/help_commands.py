from src.constants import (
    HELP_TEXT,
    EXPOSE_DATA_TEXT_PART_ONE,
    EXPOSE_DATA_TEXT_PART_TWO,
    EXPOSE_DATA_TEXT_PART_THREE,
)


def run_help_command(update, context):
    update.message.reply_markdown_v2(HELP_TEXT, quote=False)


def run_expose_data_command(update, context):
    update.message.reply_markdown_v2(EXPOSE_DATA_TEXT_PART_ONE, quote=False)
    update.message.reply_photo(
        "https://i.ibb.co/MhkhdJT/image.png",
        caption=EXPOSE_DATA_TEXT_PART_TWO,
        parse_mode="MarkdownV2",
        quote=False,
    )
    update.message.reply_photo(
        "https://i.ibb.co/y0m6kH1/image.png",
        caption=EXPOSE_DATA_TEXT_PART_THREE,
        parse_mode="MarkdownV2",
        quote=False,
    )
