from enum import Enum


class API_URI_ENDPOINTS(Enum):
    HEALTH_CHECK = "health"
    MATCHES = "matches/%s"
    PLAYERS_BY_RANK = "playersByRank"
    PLAYERS_BY_ACCOUNT_ID = "players/%s"
    HERO_STATS = "heroStats"
