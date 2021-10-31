import re


def feel_bad(update, context):
    text = update.message.text
    text_options = [
        "fuck you slarkbot",
        "fuck slarkbot",
        "shut up slarkbot",
        "shut the fuck up slarkbot",
        "bad slarkbot",
    ]
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(" +", " ", text)

    if any(x in text.lower() for x in text_options):
        update.message.reply_text("I'm sorry :(")
        update.message.reply_sticker(
            "CAACAgUAAxkBAAMfYLf_RpX-kk6gSyxd0_2gj9t9V3YAAhYCAAJfDwsGTRekwVeT3LUfBA",
            quote=False,
        )
