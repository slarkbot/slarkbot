import json
import datetime
from src import constants
from src.constants import JSON_CONSTANT_DATA_FILE_MAPPING, JSON_CONSTANT_DATA_FILE_DIR
from src.lib.endpoints import get_player_by_account_id
from telegram.utils.helpers import escape_markdown
from src.bot.services import item_services


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
    output_message = "MatchID | Hero | KDA | XPM | GPM | Result | Time Started\n"

    match = MatchDto(**match_data)

    match_id = match.match_id

    hero_id = match.hero_id
    hero_data = get_hero_data(hero_id)
    hero_name = hero_data["localized_name"]

    kda = f"%s/%s/%s" % (match.kills, match.deaths, match.assists)

    gpm = match.gold_per_min
    xpm = match.xp_per_min

    result_string = get_match_result(match.player_slot, match.radiant_win)

    start_time = convert_timestamp_to_datetime(match.start_time)

    output_message += f"{match_id} | {hero_name} | {kda} | {gpm} | {xpm} | {result_string} | {start_time}\n"

    return output_message


def create_match_detail_message(match_data):
    match_header = "Match ID | Score | Duration | Time"

    match = MatchDto(**match_data)

    player_data = [Player(**player) for player in match.players]

    game_duration = str(datetime.timedelta(seconds=match.duration))
    game_mode = constants.GAME_MODE_MAP[match.game_mode]

    score = f"{match.radiant_score}/{match.dire_score}"

    match_winner = "Radiant" if match.radiant_win else "Dire"
    match_status_text = f"The {match_winner} won a(n) {game_mode} game"
    start_time = convert_timestamp_to_datetime(match.start_time)
    match_general_text = f"{match.match_id} | {score} | {game_duration} | {start_time}"
    player_header = f"Team | Name | Hero | KDA | CS | NW | GPM | XPM"

    output_message = (
        f"{match_status_text}\n{match_header}\n{match_general_text}\n{player_header}\n"
    )

    for player in player_data:
        team = "R" if player.isRadiant else "D"

        kills = player.kills
        deaths = player.deaths
        assists = player.assists
        kda = f"{kills}/{deaths}/{assists}"

        last_hits = player.last_hits
        denies = player.denies
        cs = f"{last_hits}/{denies}"

        net_worth = player.total_gold
        xpm = player.xp_per_min
        gpm = player.gold_per_min

        account_id = player.account_id

        hero_data = get_hero_data(player.hero_id)
        hero_name = hero_data["localized_name"]

        try:
            response, status = get_player_by_account_id(account_id)
            player_name = response["profile"]["personaname"]
        except KeyError:
            player_name = "Anonymous"

        output_message += f"{team} | {player_name} | {hero_name} | {kda} | {cs} | {net_worth} | {gpm} | {xpm}\n"

    # Escape markdown up to this point
    output_message = escape_markdown(output_message, version=2)

    dotabuff_link = f"https://www.dotabuff.com/matches/{match.match_id}"
    opendota_link = f"https://www.opendota.com/matches/{match.match_id}"

    output_message += (
        f"More information: [Dotabuff]({dotabuff_link}), [OpenDota]({opendota_link})"
    )

    return output_message


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
