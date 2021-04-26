def who_asked(update, context):
    text = update.message.text

    if text == "!who":
        update.message.reply_text(
            "ɴᴏᴡ ᴘʟᴀʏɪɴɢ: Who asked (Feat: Nobody) ───────────⚪️────── ◄◄⠀▐▐⠀►► 𝟸:𝟷𝟾 / 𝟹:𝟻𝟼⠀───○ 🔊"
        )
