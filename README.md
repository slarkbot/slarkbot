
# Slark Bot

Telegram Bot for Dota2. Get DOTA statistics about matches, players, etc

The `docs` directory contains some handy documentation for various purposes.

## Prerequisites
 - Python 3.6+
 - A PostgreSQL install with the server running or docker and docker-compose
 - A Telegram account and steam account (to test your changes)

## Local Development
 - No OpenDota api key needed, however rate limits apply
 - Api documentation can be found [here](https://docs.opendota.com/#)
 - A Steam API key is required and can be found [here](https://steamcommunity.com/dev/apikey)
 - Create a bot using @BotFather in telegram to use for local development. Use the bot token in your .env file to test the bot by yourself.

### Windows Users
 - It is STRONGLY encouraged to use a linux like environment. Contributors on Windows systems use Windows subsystem for Linux (WSL).

## Installation & Environment Configuration
 - Clone or fork the repository and cd into the project root.
    * `git clone https://github.com/slarkbot/slarkbot.git && cd slarkbot`
 - Create a virtual environment using `python -m venv venv`
 - Activate virtual environment with `source venv/bin/activate` or windows equivalent
 - `pip install -r requirements.txt` to install dependencies
 - `cp .env.example .env` and change values as needed using the **Environment Variables** section below as a reference.
 - `pre-commit install` adds the lint hook to pre-push (makes it look pretty before you PR)
 - To run your local development bot, do `./main.py` or `python main.py`.
 - Message your bot in telegram with slarkbot commands like `/status` or `/changes` and you should get an OK response.

## Scripts
Scripts are made available to the command line via `setup.py`. To use these scripts, run `python setup.py install`.
The following is a short list of the scripts provided with a short description:
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

To connect and use the database, it is recommended to use DBeaver. Add a new connection and enter your connection info from your .env file.

If you are using the `psql` command line utility, be sure to specify the host, port, user, database name flags and set the PGPASSWORD environment variable. Check the `scripts` directory for examples of the structure of these commands.

### Seeding Data
 - `./scripts/seed.py` will seed hero and alias data into the slarkbot database.

## Testing
Test cases uses default Python testing module `unittest` but uses `pytest` as the test runner
 - Write your unit tests
 - From the command line `pytest`

## Slarkbot Directory Structure
 - `scripts` :: Handy scripts to manage and configure slarkbot and his database,.
 - `src` :: All of the code and logic to make slarkbot run
 - `src/bot` :: All of the logic related to bot aspect of slarkbot. This includes `bot_factory.py` which registers all of the commands, message handlers, etc and creates a `bot` object.
 - `src/constant_data` :: soon to be deprecated. Holds JSON for constant lookups.
 - `src/lib` :: API requests and responses are handled here.
 - `src/test` :: Unit tests for endpoint and API logic.
 - `src/bot/models` :: Holds ORM models used by `src/bot/services`
 - `src/bot/services` :: Data access services. Uses the SQLAlchemy ORM to perform database operations.
 - `src/bot/commands` :: Holds all of the commands for slarkbot. Anything starting with `/` is considered a command. Register these in `bot_factory.py`.
 - `src/bot/message_handlers` :: Logic to handle messages based on regex matches. When slarkbot says you're welcome after you thank him, thats a message handler.
 - `src/bot/callback_handlers` :: Used for telegram inline querying.

## Commands
Commands must preceed with `/` and match arguments given in the help text.
 - `/help` :: Show a help text describing commands and usage.
 - `/register <friend_id>` :: Register your friend ID to your telegram handle. Must be done to use some commands. Your friend ID is found on your dota profile in game.
 - `/status` :: Check to see if everything is up and running.
