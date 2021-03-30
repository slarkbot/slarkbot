#!/usr/bin/env python

import os
import json
import psycopg2
import psycopg2.extras

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DATABASE_NAME = os.getenv("POSTGRES_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
PORT = os.getenv("DATABASE_PORT")

GREEN = "\033[92m"
ENDC = "\033[0m"


def read_json(path):
    with open(path, "r") as f:
        return json.loads(f.read())


def main():
    print(f"{GREEN}READING CONSTANT DATA{ENDC}")
    heroes = read_json("src/constant_data/heroes.json")
    aliases = read_json("src/constant_data/aliases.json")

    all_aliases = []
    for alias_obj in aliases:
        for alias in alias_obj["aliases"]:
            all_aliases.append({"hero_id": alias_obj["id"], "alias": alias})

    conn_url = f"postgres://{USER}:{PASSWORD}@localhost:{PORT}/{DATABASE_NAME}"
    conn = psycopg2.connect(conn_url)
    conn.autocommit = True

    with conn.cursor() as cursor:
        print(f"{GREEN}INSERTING HEROES{ENDC}")
        psycopg2.extras.execute_batch(
            cursor,
            """
            INSERT INTO heroes VALUES (
                %(id)s,
                %(name)s,
                %(localized_name)s,
                %(primary_attr)s,
                %(roles)s
            );
        """,
            heroes,
        )

        print(f"{GREEN}INSERTING ALIASES{ENDC}")
        psycopg2.extras.execute_batch(
            cursor,
            """
            INSERT INTO hero_aliases (hero_id, alias) VALUES (
                %(hero_id)s,
                %(alias)s
            );
        """,
            all_aliases,
        )

    print(f"{GREEN}DONE{ENDC}")


if __name__ == "__main__":
    main()
