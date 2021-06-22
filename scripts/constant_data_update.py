#!/usr/bin/env python

import requests
import json

# the URLs here should be built from pre-existing constants within slarkbot
# i.e. .env and constants.py
heroesURL = "https://api.opendota.com/api/constants/heroes"
itemsURL = "https://api.opendota.com/api/constants/items"

rawHeroesData = requests.get(heroesURL).json()
rawItemsData = requests.get(itemsURL).json()

# json file mapping also exists in constants.py
# output file is just hardcoded here

# this could also be formatted as a loop in case more API fetches need to be written
with open("./src/constant_data/heroesTEST.json", "w") as outfile:
    json.dump(rawHeroesData, outfile)

with open("./src/constant_data/itemsTEST.json", "w") as outfile:
    json.dump(rawItemsData, outfile)
