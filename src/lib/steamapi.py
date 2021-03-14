import os
from steam.steamid import SteamID
from steam.webapi import WebAPI

api = WebAPI(os.getenv("STEAM_API_KEY"))


def resolve_steam_vanity_url(handle):
    response = api.call("ISteamUser.ResolveVanityURL", vanityurl=handle, url_type=1)

    if response["response"]["success"] == 1:
        return SteamID(response["response"]["steamid"]).as_32
