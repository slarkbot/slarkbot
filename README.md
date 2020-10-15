
# Dota Bot for Telegram

A bot to be like mango byte but for telegram

Get DOTA statistics about matches, players, etc


## Local Development
 - No api key needed, however rate limits apply
   - Api documentation can be found [here](https://docs.opendota.com/#)
 - Create a virtual environment using `python -m venv venv`
 - Activate virtual environment with `source venv/bin/activate` or windows equivalent
 - `pip install -r requirements.txt` to install dependencies

## Environment Configuration

 - `cp .env.example .env` and change values as needed

### Environment Variables

 - `OPEN_DOTA_API_BASE_URL` :: Base url for OpenDota API


## Testing

Test cases uses default Python testing module `unittest` but uses `pytest` as the test runner
 - Write your unit tests
 - From the command line `pytest`
