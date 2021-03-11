import os

from . import helpers


def run_changes_command(update, context):
    version = os.getenv("SLARKBOT_VERSION")
    root_dir = os.getenv("ROOT_DIR")

    file_name = f"{version}-CHANGELOG.md"

    archive_path = f"{root_dir}/archive/{file_name}"

    with open(archive_path, "r") as f:
        content = f.read()

    content = helpers.escape_markdown(content)

    update.message.reply_text(content, parse_mode="MarkdownV2")
