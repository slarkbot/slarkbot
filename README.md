
# Slark Bot

Telegram Bot for Dota2. Get DOTA statistics about matches, players, etc

The `docs` directory contains some handy documentation for various purposes.

## Local Development
 - No OpenDota api key needed, however rate limits apply
 - Api documentation can be found [here](https://docs.opendota.com/#)
 - A Steam API key is required and can be found [here](https://steamcommunity.com/dev/apikey)

### Windows Users
 - It is STRONGLY encouraged to use a linux like environment. Contributors on Windows systems use Windows subsystem for Linux (WSL).

## Installation & Environment Configuration 
 - Create a virtual environment using `python -m venv venv`
 - Activate virtual environment with `source venv/bin/activate` or windows equivalent
 - `pip install -r requirements.txt` to install dependencies
 - `cp .env.example .env` and change values as needed
 - `pre-commit install` adds the testing and lint hooks to pre-push (to make sure you do the right thing)

## Scripts
Scripts are made available to the command line via `setup.py`. To use these scripts, run `python setup.py install`.
 - `slarbot_reseed` :: Drop, recreate, and reseed the slarkbot database

Usage for these scripts are as follows:
`$ slarkbot_reseed`

## Environment Variables
 - `OPEN_DOTA_API_BASE_URL` :: Base url for OpenDota API
 - `LOG_LEVEL` :: Log level to use, defaults to `debug`. Options are info, warning, critical, error, and debug
 - `TELEGRAM_BOT_TOKEN` :: Bot token obtained from @BotFather on telegram. Used for personal development with live testing
 - `POSTGRES_USER` :: User name for the dockerized postgres instance
 - `POSTGRES_PASSWORD` :: Password for the dockerized postgres instance
 - `POSTGRES_DB` :: Name of the dockerized postgres database
 - `SLARKBOT_VERSION` :: The current semantic version of slarkbot


## Running the Database
### With Docker-compose
This option creates a postgres database in a dockerized container. Requires docker desktop
 - Run `docker-compose up -d` to bring up the container.
 - Use `docker-compose down` to stop the database server.

NOTE: If you already have a PostgreSQL server, you should utilize a different port. If you
have trouble connecting to the container, it uses 5433 rather than the default 5432. Double
check your connection info!

### With Standard PostgreSQL Server
 - Run `./scripts/standup_db.sh` from root of project directory

Use `./scripts/drop_db.sh` at any time to remove the database. This does not remove the docker volume.

### Seeding Data
 - `./scripts/seed.py` will seed hero and alias data into the slarkbot database.

## Testing
Test cases uses default Python testing module `unittest` but uses `pytest` as the test runner
 - Write your unit tests
 - From the command line `pytest`


## Commands
Commands must preceed with `/` and match arguments given in the help text.
 - `/help` :: Show a help text describing commands and usage.
 - `/register <friend_id>` :: Register your friend ID to your telegram handle. Must be done to use some commands. Your friend ID is found on your dota profile in game.
 - `/status` :: Check to see if everything is up and running.
