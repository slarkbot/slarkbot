from src.bot.models.user import User
from src.bot.models.sessions import create_session
from src.bot.services import user_services, hero_services
from src.bot.commands import helpers, match_helpers
from src.lib.steamapi import resolve_steam_vanity_url
from src.lib import endpoints
from src import constants
from steam.steamid import SteamID
from src.bot.decorators.require_registered_user_decorator import require_register
from datetime import datetime


def save_user(user):
    user.telegram_handle = user.telegram_handle.lower()
    session = create_session()
    session.merge(user)
    session.commit()


def run_register_command(update, context):
    chat_id = update.message.chat_id
    telegram_handle = update.message.from_user.username

    try:
        identifier = context.args[0]

        user = user_services.lookup_user_by_telegram_handle(telegram_handle) or User(
            telegram_handle, "", chat_id, datetime.now()
        )

        if SteamID(identifier).is_valid():
            # If the identifier is a valid steamid, convert it and done
            account_id = SteamID(identifier).as_32
        elif SteamID.from_url(identifier):
            # If the identifier is a link to a steam profile, get the id from there
            account_id = SteamID.from_url(identifier).as_32
        else:
            # Check if the Steam API gives us a valid profile
            account_id_from_vanity = resolve_steam_vanity_url(identifier)
            if account_id_from_vanity is not None:
                account_id = account_id_from_vanity

        user.account_id = account_id
        user.updated_at = datetime.now()
        save_user(user)
        update.message.reply_text(
            f"Successfully registered user {telegram_handle} as {SteamID(account_id).community_url}"
        )
    except (IndexError, ValueError):
        update.message.reply_text("No dota friend ID was given")
    except (UnboundLocalError):
        update.message.reply_text(
            "I couldn't make sense of your profile ID! You can give me a Dota friend code, a Steam ID number, a link to your Steam profile or your custom URL."
        )


def run_get_player_recents_command(update, context):
    # Assume defaults
    registered_user = user_services.lookup_user_by_telegram_handle(
        update.message.from_user.username
    )
    limit = constants.QUERY_PARAMETERS.RESPONSE_LIMIT.value

    hero_name_parts = context.args
    parts_to_remove = []

    for arg in context.args:
        user = user_services.lookup_user_by_telegram_handle(arg)
        if user:
            registered_user = user
            # If this argument is a user, remove it from hero name parts
            parts_to_remove.append(arg)

        try:
            limit = int(arg)
            # If this argument is an int, treat it as a limit
            parts_to_remove.append(arg)
        except:
            pass

    for arg in parts_to_remove:
        hero_name_parts.remove(arg)

    if not registered_user:
        update.message.reply_markdown_v2(constants.USER_NOT_REGISTERED_MESSAGE)

    account_id = registered_user.account_id

    if limit > 20:
        limit = 20

    hero_name = " ".join(hero_name_parts)
    hero_id = helpers.get_hero_id_by_name_or_alias(hero_name)

    if hero_id:
        response, status_code = endpoints.get_player_matches_by_hero_id(
            account_id, hero_id
        )
    else:
        response, status_code = endpoints.get_player_recent_matches_by_account_id(
            account_id
        )

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        update.message.reply_text(constants.BAD_RESPONSE_MESSAGE)

    output_message = match_helpers.create_recent_matches_message(response[:limit])
    update.message.reply_text(output_message)


@require_register
def run_get_player_rank_command(update, user):
    account_id = user.account_id
    response, status_code = endpoints.get_player_rank_by_account_id(account_id)

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        update.message.reply_text(constants.BAD_RESPONSE_MESSAGE)

    persona_name = response["profile"]["personaname"]
    rank_tier = response["rank_tier"]

    rank = helpers.map_rank_tier_to_string(rank_tier)

    output_message = f"{persona_name} (@{user.telegram_handle}) is {rank}"
    update.message.reply_text(output_message)


def run_get_player_hero_winrate_command(update, context):
    if not context.args:
        update.message.reply_markdown_v2(
            "No arguments given\! Try `/winrate <hero name>` or `/winrate <username> <hero name>`"
        )

    hero_name_parts = context.args
    registered_user = user_services.lookup_user_by_telegram_handle(context.args[0])

    if registered_user:
        # If there's a username in the args, remove it now
        hero_name_parts.pop(0)
    else:
        registered_user = user_services.lookup_user_by_telegram_handle(
            update.message.from_user.username
        )

    if not registered_user:
        update.message.reply_markdown_v2(constants.USER_NOT_REGISTERED_MESSAGE)

    hero_name = " ".join(hero_name_parts)
    hero_id = helpers.get_hero_id_by_name_or_alias(hero_name)

    if not hero_id:
        update.message.reply_markdown_v2(constants.USER_OR_HERO_NOT_FOUND_MESSAGE)

    response, status_code = endpoints.get_player_hero_stats(registered_user.account_id)

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        update.message.reply_text(constants.BAD_RESPONSE_MESSAGE)

    hero_data = helpers.filter_hero_winrates(response, hero_id)

    update.message.reply_text(
        helpers.format_winrate_response(hero_data, registered_user.telegram_handle)
    )


@require_register
def run_get_player_steam_profile_command(update, user):
    update.message.reply_text(
        f"@{user.telegram_handle}'s steam profile is "
        + SteamID(user.account_id).community_url
    )

@require_register
def run_player_compare_command(update, user):
    lookup_user = context.args[0]
