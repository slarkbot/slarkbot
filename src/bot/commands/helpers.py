import json
from src import constants
from src.constants import JSON_CONSTANT_DATA_FILE_MAPPING, JSON_CONSTANT_DATA_FILE_DIR


class MatchDto:
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


def get_match_result(player_slot, radiant_win):
    """
    Determines if the player (player_slot) won the game or not
    based on the boolean radiant_win
    player on radiant team :: 0   - 127
    player on dire team    :: 128 - 255
    """
    if player_slot < 128:  # on radiant team
        return "Won" if radiant_win else "Loss"
    else:  # on dire team
        return "Loss" if radiant_win else "Won"


def create_recent_matches_message(json_api_data):
    output_message = "MatchID | Hero | KDA | Result\n"

    for element in json_api_data:
        match = MatchDto(**element)

        match_id = match.match_id

        hero_id = match.hero_id
        hero_data = get_hero_data(hero_id)
        hero_name = hero_data["localized_name"]

        kda = f"%s/%s/%s" % (match.kills, match.deaths, match.assists)

        result_string = get_match_result(match.player_slot, match.radiant_win)

        output_message += f"{match_id} | {hero_name} | {kda} | {result_string}\n"

    return output_message


def create_last_match_message(match_data):
    output_message = "MatchID | Hero | KDA | XPM | GPM | Result\n"

    match = MatchDto(**match_data)

    match_id = match.match_id

    hero_id = match.hero_id
    hero_data = get_hero_data(hero_id)
    hero_name = hero_data["localized_name"]

    kda = f"%s/%s/%s" % (match.kills, match.deaths, match.assists)

    gpm = match.gold_per_min
    xpm = match.xp_per_min

    result_string = get_match_result(match.player_slot, match.radiant_win)

    output_message += (
        f"{match_id} | {hero_name} | {kda} | {gpm} | {xpm} | {result_string}\n"
    )

    return output_message
