import os
import requests
import functools


def build_url(uri):
    API_URL = os.getenv("OPEN_DOTA_API_BASE_URL")
    url = f"{API_URL}/{uri}"
    return url


def make_request(uri):
    url = build_url(uri)
    response = requests.get(url)
    return response
