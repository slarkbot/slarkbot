import unittest
from src.lib import web_scraper


class TestWebScraper(unittest.TestCase):
    def test_get_hero_counters(self):
        scraped_counters = web_scraper.get_hero_counters("ember spirit")
        self.assertIsNotNone(scraped_counters)
