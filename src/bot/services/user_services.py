from src.bot.models.user import User
from src.bot.models.sessions import create_session
from steam.steamid import SteamID
from steam.webapi import WebAPI
import os


def lookup_user_by_telegram_handle(telegram_handle):
    telegram_handle = telegram_handle.lower().replace("@", "")
    session = create_session()
    bot_user = (
        session.query(User).filter(User.telegram_handle == telegram_handle).first()
    )
    return bot_user

def resolve_steam_vanity_url(handle):
    api = WebAPI(os.getenv("STEAM_API_KEY"))
    response = api.call('ISteamUser.ResolveVanityURL', vanityurl=handle, url_type=1)

    if response['response']['success'] == 1:
        return SteamID(response['response']['steamid']).as_32
