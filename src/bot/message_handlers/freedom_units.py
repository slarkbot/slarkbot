import re


def convert_to_freedom_units(update, context):
    text = update.message.text
    match = re.findall(
        """(?:(?<=[\r\n\t\f\v ])|^)(\x2d?[0-9]*\x2e?[0-9]+[Cc])(?:(?=[\r\n\t\f\v ])|$)""",
        text,
        re.M | re.I,
    )

    if match:
        output = ""
        for group in match:
            degrees_c = float(re.findall("\x2d?[0-9]*\x2e?[0-9]+", group)[0])
            converted_units = (degrees_c * (9 / 5)) + 32

            output += f"{degrees_c} is {round(converted_units, 3)}°F in freedom units\n"

        update.message.reply_text(output)
