import re


def convert_to_freedom_units(update, context):
    text = update.message.text
    match = re.search(
        """(?:(?<=[\r\n\t\f\v ])|^)(\x2d?[0-9]*\x2e?[0-9]+[Cc])(?:(?=[\r\n\t\f\v ])|$)""",
        text,
        re.M | re.I,
    )

    print(match)

    if match:
        match = match.group(0)
        print(match)

        degrees_c = int(re.findall("\d+", match)[0])
        converted_units = (degrees_c * (9 / 5)) + 32

        output = f"{degrees_c} is {converted_units}f in freedom units"
        return update.message.reply_text(output)
