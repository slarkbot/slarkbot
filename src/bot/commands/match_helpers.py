import datetime
from src import constants
from src.lib.endpoints import get_player_by_account_id
from telegram.utils.helpers import escape_markdown
from src.bot.services import item_services
from src.bot.services import user_services
from src.bot.services import hero_services
from src.bot.commands import helpers


class MatchDto:
    def __init__(self, **kwargs):
        [setattr(self, x, i) for x, i in kwargs.items()]


class Player:
    def __init__(self, **kwargs):
        [setattr(self, x, i) for x, i in kwargs.items()]


def try_get_hero_name(hero):
    try:
        hero_name = hero.localized_name
    except:
        hero_name = "Unknown Hero"
    return hero_name


def create_recent_matches_message(json_api_data):
    output_message = "MatchID | Result | KDA | Duration | Hero\n"

    for element in json_api_data:
        match = MatchDto(**element)

        match_id = match.match_id

        hero_id = match.hero_id
        hero_data = hero_services.get_hero_by_id(hero_id)
        hero_name = try_get_hero_name(hero_data)

        kda = f"%s/%s/%s" % (match.kills, match.deaths, match.assists)

        result_string = helpers.get_match_result(match.player_slot, match.radiant_win)

        duration = str(datetime.timedelta(seconds=match.duration))

        output_message += (
            f"{match_id} | {result_string[0]} | {kda} | {duration} | {hero_name} \n"
        )

    return output_message


def create_match_message(match_data):
    match = MatchDto(**match_data)

    match_id = match.match_id

    hero_id = match.hero_id
    hero_data = hero_services.get_hero_by_id(hero_id)
    hero_name = try_get_hero_name(hero_data)

    duration = str(datetime.timedelta(seconds=match.duration))

    kda = f"%s/%s/%s" % (match.kills, match.deaths, match.assists)

    gpm = match.gold_per_min
    xpm = match.xp_per_min

    result_string = helpers.get_match_result(match.player_slot, match.radiant_win)
    game_mode = constants.GAME_MODE_MAP[match.game_mode]
    lobby_type = constants.LOBBY_TYPE_MAP[match.lobby_type]

    start_date = helpers.convert_timestamp_to_datetime(match.start_time)

    output_message = f"*{hero_name}* \| {kda} \| {gpm} GPM \| {xpm} XPM \n\n"
    output_message += f"Match ID: {match_id} \| {start_date}\n"
    output_message += f"{lobby_type} lobby \| {game_mode} game \n"
    output_message += f"Result: *{result_string}* after {duration}"

    return output_message


def create_match_detail_message(match_data, format="default"):
    match = MatchDto(**match_data)

    player_data = [Player(**player) for player in match.players]

    game_duration = str(datetime.timedelta(seconds=match.duration))
    game_mode = constants.GAME_MODE_MAP[match.game_mode]
    try:
        game_type = constants.LOBBY_TYPE_MAP[match.lobby_type]
    except:
        # Event games give an unknown ID
        game_type = "Unknown"

    score = f"{match.radiant_score} - {match.dire_score}"

    match_winner = "Radiant" if match.radiant_win else "Dire"
    start_time = helpers.convert_timestamp_to_datetime(match.start_time)

    output_message = f"Match {match.match_id} on {start_time}:\n"
    output_message += f"{game_type} lobby, {game_mode} game\n"
    output_message += f"{match_winner} victory in {game_duration}\n"
    output_message += f"{score} kills\n"

    output_message = escape_markdown(output_message, version=2)

    # Determine which content needs to be inserted
    if format == "players":
        output_message += build_players_match_message(match, player_data)
    elif format == "damage":
        output_message += build_damage_match_message(match, player_data)
    elif format == "order":
        output_message += build_pick_order_match_message(match, player_data)
    else:
        output_message += build_default_match_message(match, player_data)

    return output_message


# Default scoreboard


def build_default_match_message(match, player_data):
    # Be agnostic about the amount of players on radiant or dire, just in case
    output_message = "\nRadiant:\n"
    for player in player_data:
        if player.isRadiant:
            output_message += build_default_player_string(player)

    output_message += "\nDire:\n"
    for player in player_data:
        if not player.isRadiant:
            output_message += build_default_player_string(player)

    known_players = []

    for player in player_data:
        if player.account_id:
            bot_user = user_services.lookup_user_by_account_id(player.account_id)
            if bot_user:
                hero_data = hero_services.get_hero_by_id(player.hero_id)
                hero_name = try_get_hero_name(hero_data)

                known_players.append(f"{bot_user.telegram_handle} ({hero_name})")

    output_message += f"\nKnown players: {', '.join(known_players)}"

    # Escape markdown up to this point
    output_message = escape_markdown(output_message, version=2)

    opendota_link = f"https://www.opendota.com/matches/{match.match_id}"
    dotabuff_link = f"https://www.dotabuff.com/matches/{match.match_id}"

    output_message += f"\n\nMore information: [OpenDota]({opendota_link}), [Dotabuff]({dotabuff_link})"

    return output_message


def build_default_player_string(player):
    kills = player.kills
    deaths = player.deaths
    assists = player.assists
    kda = f"{kills}/{deaths}/{assists}"

    last_hits = player.last_hits
    denies = player.denies
    cs = f"{last_hits}/{denies}"

    level = player.level

    xpm = player.xp_per_min
    gpm = player.gold_per_min

    hero_data = hero_services.get_hero_by_id(player.hero_id)
    hero_name = try_get_hero_name(hero_data)

    return f"{kda} | L{level} | {cs} | {gpm} GPM | {xpm} XPM | {hero_name}\n"


# Players/rank view


def build_players_match_message(match, player_data):
    output_message = "\nRadiant:\n"
    for player in player_data:
        if player.isRadiant:
            output_message += build_players_player_line(player)

    output_message += "\nDire:\n"
    for player in player_data:
        if not player.isRadiant:
            output_message += build_players_player_line(player)

    output_message = escape_markdown(output_message, version=2)
    return output_message


def build_players_player_line(player):
    try:
        player_name = player.personaname
    except:
        player_name = "Anonymous"

    hero_data = hero_services.get_hero_by_id(player.hero_id)
    hero_name = try_get_hero_name(hero_data)

    if player.rank_tier:
        rank = f"| {helpers.map_rank_tier_to_string(player.rank_tier)}"
    else:
        rank = ""

    party_letter = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"][player.party_id]

    return f"{party_letter} | {player_name} ({hero_name}) {rank}\n"


# Damage and healing done


def build_damage_match_message(match, player_data):
    output_message = "\nRadiant:\n"
    for player in player_data:
        if player.isRadiant:
            output_message += build_damage_player_line(player)

    output_message += "\nDire:\n"
    for player in player_data:
        if not player.isRadiant:
            output_message += build_damage_player_line(player)

    output_message = escape_markdown(output_message, version=2)
    return output_message


def build_damage_player_line(player):
    damage = player.hero_damage
    building_damage = player.tower_damage
    healing = player.hero_healing

    hero_data = hero_services.get_hero_by_id(player.hero_id)
    hero_name = try_get_hero_name(hero_data)

    return f"{damage} DMG | {building_damage} TD | {healing} H | {hero_name}\n"


# Pick order


def build_pick_order_match_message(match, player_data):
    heroes_in_game = []
    for player in player_data:
        heroes_in_game.append(player.hero_id)

    picks_and_bans = []
    for pick_or_ban in match.picks_bans:
        picks_and_bans.append(pick_or_ban["hero_id"])

    # Filter picks and bans by heroes that actually appeared in the game
    # Everything else got banned
    picks_ordered = [pick for pick in picks_and_bans if pick in heroes_in_game]
    bans = [ban for ban in picks_and_bans if ban not in heroes_in_game]

    output_message = "\nRadiant:\n"
    for player in player_data:
        if player.isRadiant:
            output_message += build_pick_order_player_line(player, picks_ordered)

    output_message += "\nDire:\n"
    for player in player_data:
        if not player.isRadiant:
            output_message += build_pick_order_player_line(player, picks_ordered)

    banned_heroes = []
    for ban in bans:
        hero_data = hero_services.get_hero_by_id(ban)
        hero_name = try_get_hero_name(hero_data)

        banned_heroes.append(hero_name)

    output_message += "\nBans:\n"
    output_message += ", ".join(banned_heroes)

    output_message = escape_markdown(output_message, version=2)

    return output_message


def build_pick_order_player_line(player, picks_ordered):
    index = picks_ordered.index(player.hero_id)
    if index < 4:
        pick_string = "First phase"
    elif index < 8:
        pick_string = "Second phase"
    else:
        pick_string = "Last pick"

    hero_data = hero_services.get_hero_by_id(player.hero_id)
    hero_name = try_get_hero_name(hero_data)

    return f"{hero_name}: {pick_string}\n"
