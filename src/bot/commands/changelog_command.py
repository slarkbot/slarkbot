import os


def run_changes_command(update, context):
    version = os.getenv("SLARKBOT_VERSION")
    root_dir = os.getenv("ROOT_DIR")

    file_name = "%s-CHANGELOG.md" % version

    archive_path = "%s/archive/%s" % root_dir, file_name

    with open(archive_path, "r") as f:
        content = f.read()

    update.message.reply_text(content, parse_mode="MarkdownV2")
