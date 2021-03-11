def say_youre_welcome(update, context):
    text = update.message.text

    if text.lower() == "thanks slarkbot":
        update.message.reply_text("You're welcome :)")
