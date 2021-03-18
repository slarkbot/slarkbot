import os

from telegram.utils.helpers import escape_markdown


def run_changes_command(update, context):
    version = os.getenv("SLARKBOT_VERSION")
    root_dir = os.getenv("ROOT_DIR")

    file_name = f"{version}-CHANGELOG.md"

    archive_path = f"{root_dir}/archive/{file_name}"

    with open(archive_path, "r") as f:
        content = f.read()

    content = escape_markdown(content, version=2)

    update.message.reply_text(content, parse_mode="MarkdownV2")
