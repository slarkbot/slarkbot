from enum import Enum
import logging


DEFAULT_LOG_LEVEL = "debug"


USER_NOT_REGISTERED_MESSAGE = (
    "I didn't find your telegram name.. have you register or changed your telegram @?"
)


HELP_TEXT = """
    *Commands*
    `\/register <your account id here>` :: Register your telegram handle to your account id for look ups\. Example :: `\/register 55678920`\n
    `\/help` :: display this help message\n
    `\/status` :: Check to see if services are running, `OK` means everything is good to go\n
    `\/recents <limit:optional>` :: Look up your most recent matches, defaults to 5 if limit is not defined\. Must have account id registered using `/register`\. Example :: `\/recents` or `\/recents 10` for 10 most recent matches\n
    """


class API_URI_ENDPOINTS(Enum):
    HEALTH_CHECK = "health"
    MATCHES = "matches/%s"
    PLAYERS_BY_RANK = "playersByRank"
    PLAYERS_BY_ACCOUNT_ID = "players/%s"
    HERO_STATS = "heroStats"
    CONSTANTS = "constants/%s"
    PLAYER_RECENTS_BY_ACCOUNT_ID = "players/%s/recentMatches"


class QUERY_PARAMETERS(Enum):
    RESPONSE_LIMIT = 5


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


JSON_CONSTANT_DATA_FILE_DIR = "src/constant_data/"


class JSON_CONSTANT_DATA_FILE_MAPPING(Enum):
    HERO_DATA = "heroes.json"


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
    "POSTGRES_PASSWORD": {
        "required": True,
        "description": "Password for dockerized postgres instance",
    },
    "POSTGRES_USER": {
        "required": True,
        "description": "User name for dockerized postgres instance",
    },
    "POSTGRES_DB": {
        "required": True,
        "description": "Name of dockerized postgres database",
    },
    "DATABASE_PORT": {
        "required": False,
        "description": "Port to use for dockerized postgres container. Defaults to 5432",
    },
}

LOBBY_TYPE_MAP = {
    0: "Normal",
    1: "Practice",
    2: "Tournament",
    3: "Tutorial",
    4: "Coop bots",
    5: "Ranked Teams",
    6: "Ranked Solo",
    7: "Ranked",
    8: "1v1 Mid",
    9: "Battle Cup",
}

GAME_MODE_MAP = {
    0: "Unkown",
    1: "All Pick",
    2: "Captains Mode",
    3: "Random Draft",
    4: "Single Draft",
    5: "All Random",
    6: "Into",
    7: "Diretide",
    8: "Reverse Captains Mode",
    9: "Greeviling",
    10: "Tutorial",
    11: "Mid Only",
    12: "Least Played",
    13: "Limited Heroes",
    14: "Compendium Matchmaking",
    15: "Custom",
    16: "Captains Draft",
    17: "Balanced Draft",
    18: "Ability Draft",
    19: "Event",
    20: "All Random Deathmatch",
    21: "1v1 Mid",
    22: "All Draft",
    23: "Turbo",
    24: "Mutation",
}
