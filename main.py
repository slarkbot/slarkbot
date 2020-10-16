#!/usr/bin/env python

from dotenv import load_dotenv
from src.lib.endpoints import get_health_check
from src.config import check_config

if __name__ == "__main__":
    load_dotenv()
    check_config()
    response, status = get_health_check()
    print(status)
