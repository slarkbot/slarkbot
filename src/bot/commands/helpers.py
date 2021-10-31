import json
import datetime
from src import constants
from src.constants import JSON_CONSTANT_DATA_FILE_MAPPING, JSON_CONSTANT_DATA_FILE_DIR
from src.lib.endpoints import get_player_by_account_id
from telegram.utils.helpers import escape_markdown
from src.bot.services import item_services, hero_services


class MatchDto:
    def __init__(self, **kwargs):
        [setattr(self, x, i) for x, i in kwargs.items()]


class Player:
    def __init__(self, **kwargs):
        [setattr(self, x, i) for x, i in kwargs.items()]


def get_hero_id_by_name_or_alias(name_or_alias):
    hero = hero_services.get_hero_by_name(name_or_alias)
    if hero:
        return hero.id

    hero_alias = hero_services.get_hero_alias_by_name(name_or_alias)
    if hero_alias:
        return hero_alias.hero_id


def filter_hero_winrates(hero_data, hero_id):
    hero_id = str(hero_id)
    for hero in hero_data:
        if hero["hero_id"] == hero_id:
            return hero


def format_winrate_response(hero_data, telegram_handle):
    print(hero_data)
    hero_by_id = hero_services.get_hero_by_id(hero_data["hero_id"])
    hero_name = hero_by_id.localized_name
    if not hero_data["games"]:
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

    output_message += create_build_section("Start game items", mapped_start_game_items)
    output_message += create_build_section("Early game items", mapped_early_game_items)
    output_message += create_build_section("Mid game items", mapped_mid_game_items)
    output_message += create_build_section("Late game items", mapped_late_game_items)

    return output_message


def format_compare_response(first_user_data, second_user_data):
    pass
