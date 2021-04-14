import json
import datetime
from src import constants
from src.constants import JSON_CONSTANT_DATA_FILE_MAPPING, JSON_CONSTANT_DATA_FILE_DIR
from src.lib.endpoints import get_player_by_account_id
from telegram.utils.helpers import escape_markdown
from src.bot.services import item_services
from src.bot.services import user_services


class MatchDto:
    def __init__(self, **kwargs):
        [setattr(self, x, i) for x, i in kwargs.items()]


class Player:
    def __init__(self, **kwargs):
        [setattr(self, x, i) for x, i in kwargs.items()]


def read_json_file(file_path):
    with open(file_path) as data:
        data = json.load(data)
        return data


def get_hero_data(hero_id):
    hero_data_file = (
        JSON_CONSTANT_DATA_FILE_DIR + JSON_CONSTANT_DATA_FILE_MAPPING.HERO_DATA.value
    )
    hero_json = read_json_file(hero_data_file)
    for hero in hero_json:
        if hero["id"] == hero_id:
            return hero


def get_hero_by_name(hero_name):
    hero_name = hero_name.lower()

    hero_data_file = (
        JSON_CONSTANT_DATA_FILE_DIR + JSON_CONSTANT_DATA_FILE_MAPPING.HERO_DATA.value
    )
    hero_json = read_json_file(hero_data_file)
    for hero in hero_json:
        if hero["localized_name"].lower() == hero_name:
            return hero

    hero_alias_file = (
        JSON_CONSTANT_DATA_FILE_DIR + JSON_CONSTANT_DATA_FILE_MAPPING.HERO_ALIASES.value
    )
    alias_json = read_json_file(hero_alias_file)
    for hero in alias_json:
        for alias in hero["aliases"]:
            if alias.lower() == hero_name:
                found_hero = get_hero_data(hero["id"])
                return found_hero


def filter_hero_winrates(hero_data, hero_id):
    for hero in hero_data:
        if hero["hero_id"] == hero_id:
            return hero


def format_winrate_response(hero_data, telegram_handle):
    hero_by_id = get_hero_data(int(hero_data["hero_id"]))
    hero_name = hero_by_id["localized_name"]
    if hero_data["games"] == 0:
        return f"@{telegram_handle} has no games as {hero_name} recorded"

    winrate = hero_data["win"] / hero_data["games"] * 100
    winrate = round(winrate, 3)
    return f"@{telegram_handle} has a {winrate}% winrate as {hero_name} ({hero_data['win']} wins over {hero_data['games']} games)"


def convert_timestamp_to_datetime(timestamp):
    datetime_obj = datetime.datetime.fromtimestamp(timestamp)
    return datetime_obj.strftime("%m/%d/%Y")


def get_match_result(player_slot, radiant_win):
    """
    Determines if the player (player_slot) won the game or not
    based on the boolean radiant_win
    player on radiant team :: 0   - 127
    player on dire team    :: 128 - 255
    """
    if player_slot < 128:  # on radiant team
        return "Win" if radiant_win else "Loss"
    else:  # on dire team
        return "Loss" if radiant_win else "Win"


def create_recent_matches_message(json_api_data):
    output_message = "MatchID | Result | KDA | Duration | Hero\n"

    for element in json_api_data:
        match = MatchDto(**element)

        match_id = match.match_id

        hero_id = match.hero_id
        hero_data = get_hero_data(hero_id)
        hero_name = hero_data["localized_name"]

        kda = f"%s/%s/%s" % (match.kills, match.deaths, match.assists)

        result_string = get_match_result(match.player_slot, match.radiant_win)

        duration = str(datetime.timedelta(seconds = match.duration))

        output_message += (
            f"{match_id} | {result_string[0]} | {kda} | {duration} | {hero_name} \n"
        )

    return output_message


def create_match_message(match_data):
    match = MatchDto(**match_data)

    match_id = match.match_id

    hero_id = match.hero_id
    hero_data = get_hero_data(hero_id)
    hero_name = hero_data["localized_name"]

    duration = str(datetime.timedelta(seconds = match.duration))

    kda = f"%s/%s/%s" % (match.kills, match.deaths, match.assists)

    gpm = match.gold_per_min
    xpm = match.xp_per_min

    result_string = get_match_result(match.player_slot, match.radiant_win)
    game_mode = constants.GAME_MODE_MAP[match.game_mode]

    start_date = convert_timestamp_to_datetime(match.start_time)

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
    start_time = convert_timestamp_to_datetime(match.start_time)

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
                hero_data = get_hero_data(player.hero_id)
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
                response, status = get_player_by_account_id(player.account_id)
                player_name = response["profile"]["personaname"]
            except KeyError:
                player_name = "Anonymous"
            
            hero_data = get_hero_data(player.hero_id)
            hero_name = hero_data["localized_name"]

            if player.rank_tier:
                rank = f"- {map_rank_tier_to_string(player.rank_tier)}"
            else:
                rank = ""

            output_message += f"{player_name} ({hero_name}) {rank}\n"
    
    output_message += "\nDire:\n"
    for player in player_data:
        if not player.isRadiant:
            try:
                response, status = get_player_by_account_id(player.account_id)
                player_name = response["profile"]["personaname"]
            except KeyError:
                player_name = "Anonymous"
            
            hero_data = get_hero_data(player.hero_id)
            hero_name = hero_data["localized_name"]

            if player.rank_tier:
                rank = f"- {map_rank_tier_to_string(player.rank_tier)}"
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

    hero_data = get_hero_data(player.hero_id)
    hero_name = hero_data["localized_name"]

    return f"{kda} | {cs} | {gpm} GPM | {xpm} XPM | {hero_name}\n"

def map_rank_tier_to_string(rank):
    # ranks are two digit codes
    # mapper values for first digit are found in constants.RANKS

    print(rank)

    if not rank:
        return "not calibrated"

    if rank == 80:
        return "Immortal"

    # get last digit
    rank_copy = rank
    tier = rank_copy % 10

    # get first digit
    while rank >= 10:
        rank = rank / 10

    rank = int(rank)

    print(tier)

    medal = constants.RANKS[rank]

    return f"{medal} {tier}"


def find_three_most_bought_items_in_item_data(item_data):
    return sorted(item_data, key=item_data.get, reverse=True)[:3]


def map_item_ids_to_item_names(item_ids):
    mapped_names = []
    for item_id in item_ids:
        item = item_services.get_item_by_id(item_id)

        if item:
            mapped_names.append(item.item_name)

    return mapped_names


def create_build_section(header_title, data):
    header = f"**{header_title}**"
    data_field = " -> ".join(data)
    escaped_data = escape_markdown(data_field, version=2)
    return f"{header}\n{escaped_data}\n"


def create_suggested_build_message(hero_name, item_data):
    hero_name = escape_markdown(hero_name, version=2)

    start_game_items = item_data["start_game_items"]
    early_game_items = item_data["early_game_items"]
    mid_game_items = item_data["mid_game_items"]
    late_game_items = item_data["late_game_items"]

    most_bought_start_game_items = find_three_most_bought_items_in_item_data(
        start_game_items
    )
    most_bought_early_game_items = find_three_most_bought_items_in_item_data(
        early_game_items
    )
    most_bought_mid_game_items = find_three_most_bought_items_in_item_data(
        mid_game_items
    )
    most_bought_late_game_items = find_three_most_bought_items_in_item_data(
        late_game_items
    )

    mapped_start_game_items = map_item_ids_to_item_names(most_bought_start_game_items)
    mapped_early_game_items = map_item_ids_to_item_names(most_bought_early_game_items)
    mapped_mid_game_items = map_item_ids_to_item_names(most_bought_mid_game_items)
    mapped_late_game_items = map_item_ids_to_item_names(most_bought_late_game_items)

    output_message = f"Recommended items for {hero_name}\n"

    # output_message += "**Start game items**\n"
    # output_message += " -> ".join(mapped_start_game_items)

    output_message += create_build_section("Start game items", mapped_start_game_items)
    output_message += create_build_section("Early game items", mapped_early_game_items)
    output_message += create_build_section("Mid game items", mapped_mid_game_items)
    output_message += create_build_section("Late game items", mapped_late_game_items)

    return output_message
