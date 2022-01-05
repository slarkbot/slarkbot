import re


def say_youre_welcome(update, context):
    text = update.message.text
    text_options = [
        "thanks slarkbot",
        "thank you slarkbot",
        "thanksies slarkbot",
        "thamks slarkbot",
    ]
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(" +", " ", text)

    if any(x in text.lower() for x in text_options):
        update.message.reply_text("You're welcome :)")
        update.message.reply_sticker(
            "CAACAgQAAx0CPjTD9AABC2m9YLfsTcojjSPl7L_DFbWS3IWrp34AAocAA_tjggqQUNMScJneeB8E",
            quote=False,
        )
