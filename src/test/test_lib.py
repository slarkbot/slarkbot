import unittest
import os
from dotenv import load_dotenv

from . import well_known_data

from src.lib import endpoints
from src.lib import request


class TestEndpoints(unittest.TestCase):
    def setUp(self):
        load_dotenv()

    def test_get_health_check(self):
        response, status_code = endpoints.get_health_check()
        self.assertEqual(status_code, 200)

    def test_get_match_by_id(self):
        match_id = well_known_data.TEST_MATCH_ID
        response, status_code = endpoints.get_match_by_id(match_id)
        self.assertEqual(status_code, 200)

    def test_get_players_by_rank(self):
        response, status_code = endpoints.get_players_by_rank()
        self.assertEqual(status_code, 200)


class TestRequest(unittest.TestCase):
    def setUp(self):
        load_dotenv()

    def test_build_url(self):
        uri = "data"
        actual = request.build_url(uri)
        expected = f'{os.getenv("OPEN_DOTA_API_BASE_URL")}/data'
        self.assertEqual(actual, expected)
