from enum import Enum
import logging


DEFAULT_LOG_LEVEL = "debug"


class API_URI_ENDPOINTS(Enum):
    HEALTH_CHECK = "health"
    MATCHES = "matches/%s"
    PLAYERS_BY_RANK = "playersByRank"
    PLAYERS_BY_ACCOUNT_ID = "players/%s"
    HERO_STATS = "heroStats"
    CONSTANTS = "constants/%s"


class HTTP_STATUS_CODES(Enum):
    OK = 200
    NOT_FOUND = 404
    BAD_REQUEST = 400


LOG_LEVEL_MAP = {
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
    "debug": logging.DEBUG,
}


ENVIRONMENT_VARIABLES_CONFIG = {
    "OPEN_DOTA_API_BASE_URL": {
        "required": True,
        "description": "Base URL for hitting the API endpoints",
    },
    "TELEGRAM_BOT_TOKEN": {
        "required": True,
        "description": "Telegram bot token, can be used for local development",
    },
    "LOG_LEVEL": {
        "required": False,
        "description": "Logging level. Defaults to `debug`",
    },
}
