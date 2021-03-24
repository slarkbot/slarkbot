from src.lib import endpoints
from src.constants import HTTP_STATUS_CODES


def run_health_check(update, context):
    response, status_code = endpoints.get_health_check()

    if status_code != HTTP_STATUS_CODES.OK.value:
        text = "Health check resulted in %s error code with response %s" % (
            status_code,
            response,
        )
    else:
        text = "Health check passed OK"

    update.message.reply_text(text)
