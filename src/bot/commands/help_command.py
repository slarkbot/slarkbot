from src.constants import HELP_TEXT


def run_help_command(update, context):
    update.message.reply_markdown_v2(HELP_TEXT, quote=False)
