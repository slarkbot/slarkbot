
import re

def whats_dn(update, context):
    text = update.message.text
    search_for = "dn"

    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(" +", " ", text)

    if any(x in text.lower() for x in search_for):
        update.message.reply_text("What's DN?")
