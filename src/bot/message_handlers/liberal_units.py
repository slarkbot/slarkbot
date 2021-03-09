import re


def convert_to_liberal_units(update, context):
    text = update.message.text
    match = re.search(
        """(?:(?<=[\r\n\t\f\v ])|^)(\x2d?[0-9]*\x2e?[0-9]+[Ff])(?:(?=[\r\n\t\f\v ])|$)""",
        text,
        re.M | re.I,
    )

    if match:
        match = match.group(0)

        degrees_f = float(re.findall("\x2d?[0-9]*\x2e?[0-9]+", match)[0])
        converted_units = (degrees_f - 32) * 5 / 9

        output = f"{degrees_f} is {converted_units}°C in liberal units"
        update.message.reply_text(output)
