
import unittest
from dotenv import load_dotenv

from src.lib import health_check

class TestLibrary(unittest.TestCase):

    def setUp(self):
        load_dotenv()

    def test_get_health_check(self):
        response, status_code = health_check.get_health_check()
        self.assertEqual(status_code, 200)
