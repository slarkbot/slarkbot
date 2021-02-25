
def say_youre_welcome(update, context):
    text = update.message.text

    print("TEXT ", text)
    
    if text.lower() is "thanks slarkbot":
        update.message.reply_text("You're welcome :)")
