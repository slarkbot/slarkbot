import requests
from bs4 import BeautifulSoup
from src import constants
from pprint import pprint


def get_hero_counters(hero_name):
    hero_name = hero_name.replace(" ", "-").lower()

    uri = constants.WEB_SCRAPER_URIS.COUNTERS.value % hero_name

    response = requests.get(uri, headers=constants.WEBSCRAPER_USER_AGENT_HEADER)

    if response.status_code != 200:
        return None

    raw_html = response.text

    processed_html = BeautifulSoup(raw_html, "html.parser")

    counter_table_rows = processed_html.find_all("table")[1].contents[1].contents

    hero_counters = []
    for row in counter_table_rows:

        hero = []
        for data_column in row:
            if data_column.has_attr("style"):
                continue

            hero.append(data_column["data-value"])

        hero_counters.append(hero)

    return hero_counters
