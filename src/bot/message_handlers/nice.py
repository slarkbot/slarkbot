import re


def say_nice(update, context):
    text = update.message.text

    match = re.search(
        "(69|420)",
        text,
        re.M | re.I,
    )

    if match:
        update.message.reply_text("nice")
