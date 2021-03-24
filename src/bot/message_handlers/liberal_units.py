import re


def convert_to_liberal_units(update, context):
    text = update.message.text
    match = re.findall(
        """(?:(?<=[\r\n\t\f\v ])|^)(\x2d?[0-9]*\x2e?[0-9]+[Ff])(?:(?=[\r\n\t\f\v ])|$)""",
        text,
        re.M | re.I,
    )

    if match:
        output = ""
        for group in match:
            degrees_f = float(re.findall("\x2d?[0-9]*\x2e?[0-9]+", group)[0])
            converted_units = (degrees_f - 32) * 5 / 9

            output += f"{degrees_f} is {round(converted_units, 3)}°C in liberal units\n"
        update.message.reply_text(output)
