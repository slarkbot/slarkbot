#!/usr/bin/env python

from dotenv import load_dotenv
from src.lib.endpoints import get_health_check

if __name__ == "__main__":
    load_dotenv()
    get_health_check()
