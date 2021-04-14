import json
import datetime
from src import constants
from src.constants import JSON_CONSTANT_DATA_FILE_MAPPING, JSON_CONSTANT_DATA_FILE_DIR
from src.lib.endpoints import get_player_by_account_id
from telegram.utils.helpers import escape_markdown
from src.bot.services import item_services
from src.bot.services import user_services
from src.bot.commands import helpers


class MatchDto:
    def __init__(self, **kwargs):
        [setattr(self, x, i) for x, i in kwargs.items()]


class Player:
    def __init__(self, **kwargs):
        [setattr(self, x, i) for x, i in kwargs.items()]


def create_recent_matches_message(json_api_data):
    output_message = "MatchID | Result | KDA | Duration | Hero\n"

    for element in json_api_data:
        match = MatchDto(**element)

        match_id = match.match_id

        hero_id = match.hero_id
        hero_data = helpers.get_hero_data(hero_id)
        hero_name = hero_data["localized_name"]

        kda = f"%s/%s/%s" % (match.kills, match.deaths, match.assists)

        result_string = helpers.get_match_result(match.player_slot, match.radiant_win)

        duration = str(datetime.timedelta(seconds = match.duration))

        output_message += (
            f"{match_id} | {result_string[0]} | {kda} | {duration} | {hero_name} \n"
        )

    return output_message


def create_match_message(match_data):
    match = MatchDto(**match_data)

    match_id = match.match_id

    hero_id = match.hero_id
    hero_data = helpers.get_hero_data(hero_id)
    hero_name = hero_data["localized_name"]

    duration = str(datetime.timedelta(seconds = match.duration))

    kda = f"%s/%s/%s" % (match.kills, match.deaths, match.assists)

    gpm = match.gold_per_min
    xpm = match.xp_per_min

    result_string = helpers.get_match_result(match.player_slot, match.radiant_win)
    game_mode = constants.GAME_MODE_MAP[match.game_mode]

    start_date = helpers.convert_timestamp_to_datetime(match.start_time)

    output_message  = f"*{hero_name}* \| {kda} \| {gpm} GPM \| {xpm} XPM \n\n"
    output_message += f"Match ID: {match_id} \| {start_date} \| {game_mode} \n"
    output_message += f"Result: *{result_string}* after {duration}"

    return output_message


def create_match_detail_message(match_data, format = "default"):
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

    output_message  = f"Match {match.match_id} on {start_time}:\n"
    output_message += f"{game_type} lobby, {game_mode} game\n"
    output_message += f"{match_winner} victory in {game_duration}\n"
    output_message += f"{score} kills\n"

    output_message = escape_markdown(output_message, version=2)

    # Determine which content needs to be inserted
    if format == "players":
        output_message += build_players_match_message(match, player_data)
    else:
        output_message += build_default_match_message(match, player_data)

    return output_message

def build_default_match_message(match, player_data):
    # Be agnostic about the amount of players on radiant or dire, just in case
    output_message = "\nRadiant:\n"
    for player in player_data:
        if player.isRadiant:
            output_message += build_player_string(player)
    
    output_message += "\nDire:\n"
    for player in player_data:
        if not player.isRadiant:
            output_message += build_player_string(player)

    known_players = []

    for player in player_data:
        if player.account_id:
            bot_user = user_services.lookup_user_by_account_id(player.account_id)
            if bot_user:
                hero_data = helpers.get_hero_data(player.hero_id)
                hero_name = hero_data["localized_name"]
                
                known_players.append(f"{bot_user.telegram_handle} ({hero_name})")

    output_message += f"\nKnown players: {', '.join(known_players)}"

    # Escape markdown up to this point
    output_message = escape_markdown(output_message, version=2)

    opendota_link = f"https://www.opendota.com/matches/{match.match_id}"
    dotabuff_link = f"https://www.dotabuff.com/matches/{match.match_id}"

    output_message += (
        f"\n\nMore information: [OpenDota]({opendota_link}), [Dotabuff]({dotabuff_link})"
    )

    return output_message

def build_players_match_message(match, player_data):
    output_message = "\nRadiant:\n"
    for player in player_data:
        if player.isRadiant:
            try:
                response, status = helpers.get_player_by_account_id(player.account_id)
                player_name = response["profile"]["personaname"]
            except KeyError:
                player_name = "Anonymous"
            
            hero_data = helpers.get_hero_data(player.hero_id)
            hero_name = hero_data["localized_name"]

            if player.rank_tier:
                rank = f"| {helpers.map_rank_tier_to_string(player.rank_tier)}"
            else:
                rank = ""

            output_message += f"{player_name} ({hero_name}) {rank}\n"
    
    output_message += "\nDire:\n"
    for player in player_data:
        if not player.isRadiant:
            try:
                response, status = helpers.get_player_by_account_id(player.account_id)
                player_name = response["profile"]["personaname"]
            except KeyError:
                player_name = "Anonymous"
            
            hero_data = helpers.get_hero_data(player.hero_id)
            hero_name = hero_data["localized_name"]

            if player.rank_tier:
                rank = f"| {helpers.map_rank_tier_to_string(player.rank_tier)}"
            else:
                rank = ""

            output_message += f"{player_name} ({hero_name}) {rank}\n"

    output_message = escape_markdown(output_message, version=2)
    return output_message

def build_player_string(player):
    kills = player.kills
    deaths = player.deaths
    assists = player.assists
    kda = f"{kills}/{deaths}/{assists}"

    last_hits = player.last_hits
    denies = player.denies
    cs = f"{last_hits}/{denies}"

    xpm = player.xp_per_min
    gpm = player.gold_per_min

    hero_data = helpers.get_hero_data(player.hero_id)
    hero_name = hero_data["localized_name"]

    return f"{kda} | {cs} | {gpm} GPM | {xpm} XPM | {hero_name}\n"
